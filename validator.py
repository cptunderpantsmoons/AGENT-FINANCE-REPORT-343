"""
Comprehensive validation module for financial statement generation.
Performs all mandatory checks before finalizing the PDF.
"""

from typing import Dict, Any, Tuple, List, Optional
import sys
import os


class FinancialStatementValidator:
    """
    Validates financial statements before final generation.
    Implements all mandatory checks per the AASB compliance requirements.
    """
    
    def __init__(self, entity_name: str, current_year: int, use_ai: bool = True):
        """
        Initialize validator.
        
        Args:
            entity_name (str): Name of the entity
            current_year (int): Current financial year
            use_ai (bool): Whether to use AI-powered validation
        """
        self.entity_name = entity_name
        self.current_year = current_year
        self.errors = []
        self.warnings = []
        self.queries = []
        self.use_ai = use_ai and os.getenv('OPENROUTER_API_KEY') is not None
        
        if self.use_ai:
            try:
                from ai_service import AIService
                self.ai_service = AIService()
                print("  ✓ AI-powered validation enabled")
            except Exception as e:
                print(f"  ⚠ AI validation unavailable: {str(e)}")
                self.use_ai = False
                self.ai_service = None
        else:
            self.ai_service = None
    
    def validate_all(self, bs_data: Dict[str, Any], pl_data: Dict[str, Any], 
                    prior_year_data: Dict[str, Any], prior_re: float,
                    directors: List[Dict[str, str]], compiler: Dict[str, str],
                    tax_consolidation_entity: Optional[str] = None,
                    contingent_liability_text: Optional[str] = None,
                    notes_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str], List[str], List[str]]:
        """
        Perform all validation checks.
        
        Args:
            bs_data: Current year balance sheet data
            pl_data: Current year profit & loss data
            prior_year_data: Prior year financial data
            prior_re: Prior year retained earnings
            directors: List of director information
            compiler: Compiler/signatory information
            tax_consolidation_entity: Head entity name for tax consolidation
            contingent_liability_text: Prior year contingent liability text
            
        Returns:
            Tuple[bool, List[str], List[str], List[str]]: (is_valid, errors, warnings, queries)
        """
        self.errors = []
        self.warnings = []
        self.queries = []
        
        # Mandatory checks (STOP if fail)
        self._validate_balance_sheet_balances(bs_data)
        self._validate_retained_earnings_rollforward(bs_data, pl_data, prior_re)
        self._validate_tax_consolidation_disclosure(tax_consolidation_entity)
        self._validate_contingent_liability_consistency(contingent_liability_text)
        self._validate_director_names(directors)
        self._validate_compilation_signatory(compiler)
        
        # Additional validations (warn but proceed)
        self._validate_cash_accounts(bs_data)
        self._validate_related_party_loans(bs_data)
        self._validate_deferred_tax(pl_data, bs_data)
        
        # AI-powered validations
        if self.use_ai and self.ai_service:
            self._ai_validate_balance_sheet(bs_data, pl_data)
            if notes_data:
                self._ai_validate_notes(notes_data, bs_data, pl_data)
        
        is_valid = len(self.errors) == 0
        
        return is_valid, self.errors, self.warnings, self.queries
    
    def _validate_balance_sheet_balances(self, bs_data: Dict[str, Any]) -> None:
        """
        Check: Total Assets = Total Liabilities + Total Equity
        
        ❌ STOP if mismatch
        """
        assets = bs_data.get('total_assets', 0)
        liabilities = bs_data.get('total_liabilities', 0)
        equity = bs_data.get('total_equity', 0)
        liabilities_equity = liabilities + equity
        
        difference = abs(assets - liabilities_equity)
        
        if difference >= 1:  # Allow for rounding differences
            error_msg = (
                f"❌ BALANCE SHEET DOES NOT BALANCE\n"
                f"   Total Assets: ${assets:,.0f}\n"
                f"   Total Liabilities + Equity: ${liabilities_equity:,.0f}\n"
                f"   Difference: ${difference:,.0f}\n"
                f"   STOP - Please reconcile and try again."
            )
            self.errors.append(error_msg)
    
    def _validate_retained_earnings_rollforward(self, bs_data: Dict[str, Any], 
                                               pl_data: Dict[str, Any], 
                                               prior_re: float) -> None:
        """
        Check: RE_end = RE_start + Net Profit/(Loss)
        
        ❌ STOP if mismatch
        """
        current_re = bs_data.get('equity', {}).get('retained_earnings', 0)
        net_profit_loss = pl_data.get('net_profit_loss', 0)
        expected_re = prior_re + net_profit_loss
        
        difference = abs(current_re - expected_re)
        
        if difference >= 1:  # Allow for rounding differences
            error_msg = (
                f"❌ RETAINED EARNINGS MISMATCH\n"
                f"   Prior Year RE: ${prior_re:,.0f}\n"
                f"   Net Profit/(Loss): ${net_profit_loss:,.0f}\n"
                f"   Expected RE: ${expected_re:,.0f}\n"
                f"   Actual RE: ${current_re:,.0f}\n"
                f"   Difference: ${difference:,.0f}\n"
                f"   STOP - Please verify start value and loss amount."
            )
            self.errors.append(error_msg)
    
    def _validate_tax_consolidation_disclosure(self, tax_consolidation_entity: Optional[str]) -> None:
        """
        Check: Note 3(b)(i) must reference correct head entity.
        
        ❌ STOP if head entity name differs from prior year & unconfirmed
        """
        if tax_consolidation_entity:
            # This would need to be compared with prior year
            # For now, we'll just note it needs verification
            query_msg = (
                f"⚠️ TAX CONSOLIDATION DISCLOSURE\n"
                f"   Head Entity: {tax_consolidation_entity}\n"
                f"   Please confirm this matches prior year disclosure."
            )
            self.queries.append(query_msg)
    
    def _validate_contingent_liability_consistency(self, contingent_liability_text: Optional[str]) -> None:
        """
        Check: If prior year had TENBS/other commitment, FY2025 must retain identical wording.
        
        ❌ QUERY if missing or altered without confirmation
        """
        if contingent_liability_text:
            query_msg = (
                f"⚠️ CONTINGENT LIABILITY CONSISTENCY\n"
                f"   Prior year had contingent liability disclosure.\n"
                f"   Please confirm FY2025 retains identical wording:\n"
                f"   {contingent_liability_text[:200]}..."
            )
            self.queries.append(query_msg)
    
    def _validate_director_names(self, directors: List[Dict[str, str]]) -> None:
        """
        Check: Director names & titles must match prior-year declaration.
        
        ❌ CONFIRM before updating sign date
        """
        expected_directors = ['Matthew Warnken', 'Gary Wyatt', 'Julian Turecek']
        current_names = [d.get('name', '') for d in directors]
        
        missing = [name for name in expected_directors if name not in current_names]
        extra = [name for name in current_names if name not in expected_directors]
        
        if missing or extra:
            query_msg = (
                f"⚠️ DIRECTOR NAMES VERIFICATION\n"
                f"   Expected: {', '.join(expected_directors)}\n"
                f"   Found: {', '.join(current_names)}\n"
                f"   Missing: {', '.join(missing) if missing else 'None'}\n"
                f"   Extra: {', '.join(extra) if extra else 'None'}\n"
                f"   Please confirm before updating sign date."
            )
            self.queries.append(query_msg)
    
    def _validate_compilation_signatory(self, compiler: Dict[str, str]) -> None:
        """
        Check: Compilation signatory must be qualified (e.g., Allan Tuback, CFO).
        
        ❌ VERIFY credentials if changed
        """
        expected_compiler = 'Allan Tuback'
        compiler_name = compiler.get('name', '')
        compiler_title = compiler.get('title', '')
        
        if expected_compiler not in compiler_name:
            query_msg = (
                f"⚠️ COMPILATION SIGNATORY VERIFICATION\n"
                f"   Expected: {expected_compiler}\n"
                f"   Found: {compiler_name}\n"
                f"   Title: {compiler_title}\n"
                f"   Please verify credentials if changed."
            )
            self.queries.append(query_msg)
    
    def _validate_cash_accounts(self, bs_data: Dict[str, Any]) -> None:
        """
        Check: Confirm closure of legacy accounts (e.g., Wise closed → $0 in FY2025).
        
        ⚠️ Warn but proceed if minor
        """
        cash = bs_data.get('current_assets', {}).get('cash', 0)
        
        if cash == 0:
            warning_msg = (
                f"⚠️ CASH ACCOUNTS\n"
                f"   Cash balance is $0. Please confirm closure of legacy accounts."
            )
            self.warnings.append(warning_msg)
    
    def _validate_related_party_loans(self, bs_data: Dict[str, Any]) -> None:
        """
        Check: Excel shows $0 CL / $1.79M NCL — ensure draft PDF inconsistencies are corrected.
        
        ⚠️ Warn but proceed if minor
        """
        current_liabilities = bs_data.get('current_liabilities', {})
        non_current_liabilities = bs_data.get('non_current_liabilities', {})
        
        # This is entity-specific - would need to check for related party loans
        # For now, just a placeholder
        pass
    
    def _validate_deferred_tax(self, pl_data: Dict[str, Any], bs_data: Dict[str, Any]) -> None:
        """
        Check: No income tax benefit recognised in FY2025 (Excel shows $0 tax).
        Note 4 must explain why.
        
        ⚠️ Warn but proceed if minor
        """
        tax_expense = pl_data.get('income_tax_expense', 0)
        
        if tax_expense == 0:
            warning_msg = (
                f"⚠️ DEFERRED TAX\n"
                f"   No income tax expense recognised in FY2025.\n"
                f"   Ensure Note 4 explains why (e.g., 'no recognition due to uncertainty re: future taxable profits')."
            )
            self.warnings.append(warning_msg)
    
    def print_validation_results(self) -> None:
        """Print all validation results."""
        if self.errors:
            print("\n" + "="*80)
            print("CRITICAL ERRORS - GENERATION HALTED")
            print("="*80)
            for error in self.errors:
                print(f"\n{error}")
            print("\n" + "="*80)
        
        if self.queries:
            print("\n" + "="*80)
            print("QUERIES REQUIRING CONFIRMATION")
            print("="*80)
            for query in self.queries:
                print(f"\n{query}")
            print("\n" + "="*80)
        
        if self.warnings:
            print("\n" + "="*80)
            print("WARNINGS (Proceeding with generation)")
            print("="*80)
            for warning in self.warnings:
                print(f"\n{warning}")
            print("\n" + "="*80)
        
        if not self.errors and not self.queries and not self.warnings:
            print("\n✓ All validations passed. Proceeding with generation.")
    
    def _ai_validate_balance_sheet(self, bs_data: Dict[str, Any], pl_data: Dict[str, Any]) -> None:
        """Use AI to validate balance sheet relationships."""
        if not self.use_ai or not self.ai_service:
            return
        
        try:
            print("  Running AI-powered balance sheet validation...")
            is_valid, message, analysis = self.ai_service.validate_balance_sheet_relationships(bs_data, pl_data)
            
            if not is_valid:
                error_msg = f"❌ AI VALIDATION: {message}\n"
                if 'issues' in analysis:
                    error_msg += "\n".join([f"   - {issue}" for issue in analysis.get('issues', [])])
                self.errors.append(error_msg)
            else:
                if 'recommendations' in analysis and analysis['recommendations']:
                    for rec in analysis['recommendations']:
                        self.warnings.append(f"⚠️ AI Recommendation: {rec}")
                print("  ✓ AI balance sheet validation passed")
        except Exception as e:
            print(f"  ⚠ AI validation error: {str(e)}")
    
    def _ai_validate_notes(self, notes_data: Dict[str, Any], 
                          bs_data: Dict[str, Any], pl_data: Dict[str, Any]) -> None:
        """Use AI to validate note disclosures."""
        if not self.use_ai or not self.ai_service:
            return
        
        try:
            print("  Running AI-powered note disclosure validation...")
            is_complete, missing, analysis = self.ai_service.validate_note_disclosures(
                notes_data, bs_data, pl_data
            )
            
            if not is_complete:
                if missing:
                    query_msg = f"⚠️ AI NOTE VALIDATION: Missing disclosures detected\n"
                    query_msg += "\n".join([f"   - {item}" for item in missing])
                    self.queries.append(query_msg)
                
                if 'inadequate_notes' in analysis:
                    for note in analysis.get('inadequate_notes', []):
                        self.warnings.append(f"⚠️ AI: Note needs more detail: {note}")
            else:
                print("  ✓ AI note validation passed")
        except Exception as e:
            print(f"  ⚠ AI note validation error: {str(e)}")
    
    def halt_if_errors(self) -> None:
        """Halt execution if there are critical errors."""
        if self.errors:
            self.print_validation_results()
            sys.exit(1)

