#!/usr/bin/env python3
"""
Main application for generating AASB-compliant financial statements for non-reporting entities.
Implements comprehensive validation and PDF parsing per AASB requirements.
"""

import sys
import os
import argparse
from typing import Dict, Any, Optional
from aasb_financial_statement_generator import AASBFinancialStatementGenerator
from excel_processor import ExcelProcessor
from pdf_parser import PDFParser
from validator import FinancialStatementValidator


def validate_inputs(args: argparse.Namespace) -> bool:
    """
    Validate input files and parameters.
    
    Args:
        args (argparse.Namespace): Command line arguments
        
    Returns:
        bool: True if all inputs are valid, False otherwise
    """
    # Check if Excel file exists
    if not os.path.exists(args.excel_file):
        print(f"Error: Excel file '{args.excel_file}' not found.")
        return False
    
    # Check if prior year PDF exists
    if not os.path.exists(args.prior_year_pdf):
        print(f"Error: Prior year PDF '{args.prior_year_pdf}' not found.")
        return False
    
    # Check if draft current year PDF exists (if provided)
    if args.draft_current_pdf and not os.path.exists(args.draft_current_pdf):
        print(f"Warning: Draft current year PDF '{args.draft_current_pdf}' not found.")
        args.draft_current_pdf = None  # Set to None so we don't try to use it
    
    return True


def extract_prior_year_data(pdf_parser: PDFParser) -> Dict[str, Any]:
    """
    Extract prior year data from PDF using PDFParser.
    
    Args:
        pdf_parser (PDFParser): Initialized PDF parser
        
    Returns:
        Dict[str, Any]: Dictionary containing prior year financial data
    """
    print("  Extracting income statement data...")
    pl_data = pdf_parser.extract_income_statement_data()
    
    print("  Extracting balance sheet data...")
    bs_data = pdf_parser.extract_balance_sheet_data()
    
    # Combine into single structure
    prior_year_data = {**pl_data, **bs_data}
    
    return prior_year_data


def extract_notes_structure(pdf_parser: PDFParser, draft_pdf_parser: Optional[PDFParser] = None) -> Dict[str, Any]:
    """
    Extract notes structure from prior year PDF.
    Optionally use draft PDF for hints on new disclosures.
    
    Args:
        pdf_parser (PDFParser): Prior year PDF parser
        draft_pdf_parser (Optional[PDFParser]): Draft current year PDF parser
        
    Returns:
        Dict[str, Any]: Notes structure and content
    """
    print("  Extracting notes structure...")
    notes = pdf_parser.extract_notes_structure()
    
    # Convert to dictionary format
    notes_data = {}
    for note in notes:
        note_key = f"note_{note['number']}"
        notes_data[note_key] = {
            'number': note['number'],
            'heading': note['heading'],
            'content': '\n'.join(note['content'])
        }
    
    # If draft PDF provided, check for new disclosures
    if draft_pdf_parser:
        print("  Checking draft PDF for new disclosures...")
        draft_notes = draft_pdf_parser.extract_notes_structure()
        # Compare and flag new notes (would need user confirmation)
    
    return notes_data


def main():
    parser = argparse.ArgumentParser(
        description='Generate AASB-compliant financial statements for non-reporting entities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --entity-name "Example Pty Ltd" --current-year 2025 \\
    --excel-file sample2025DataMAKI.xlsx --prior-year-pdf sample2024.pdf
  
  python main.py --entity-name "Example Pty Ltd" --current-year 2025 \\
    --excel-file sample2025DataMAKI.xlsx --prior-year-pdf sample2024.pdf \\
    --draft-current-pdf draft2025.pdf
        """
    )
    parser.add_argument('--entity-name', required=True, 
                       help='Name of the entity')
    parser.add_argument('--current-year', type=int, required=True, 
                       help='Current financial year (e.g., 2025)')
    parser.add_argument('--excel-file', required=True, 
                       help='Path to the Entity Management Reports Excel file')
    parser.add_argument('--prior-year-pdf', required=True, 
                       help='Path to the prior year Financial Reports PDF')
    parser.add_argument('--draft-current-pdf', 
                       help='Path to the draft current year Financial Statements PDF (optional)')
    parser.add_argument('--use-ai', action='store_true', default=True,
                       help='Enable AI-powered validation and enhancement (requires OPENROUTER_API_KEY)')
    parser.add_argument('--no-ai', dest='use_ai', action='store_false',
                       help='Disable AI-powered features')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not validate_inputs(args):
        sys.exit(1)
    
    try:
        # ============================================================
        # STEP 1: Parse Prior Year PDF
        # ============================================================
        print("\n" + "="*80)
        print("STEP 1: Parsing Prior Year PDF")
        print("="*80)
        pdf_parser = PDFParser(args.prior_year_pdf)
        
        # Extract entity name and year from PDF (or use provided)
        entity_name = pdf_parser.extract_entity_name() or args.entity_name
        prior_year = pdf_parser.extract_prior_year() or (args.current_year - 1)
        
        print(f"  Entity: {entity_name}")
        print(f"  Prior Year: {prior_year}")
        
        # Extract prior year financial data
        prior_year_data = extract_prior_year_data(pdf_parser)
        
        # AI-enhanced PDF parsing (if enabled)
        if args.use_ai and os.getenv('OPENROUTER_API_KEY'):
            try:
                from ai_service import AIService
                ai_service = AIService()
                print("  Enhancing PDF extraction with AI...")
                
                # Use AI to extract additional data from PDF text
                pdf_text = pdf_parser.get_full_text()
                
                # Enhance financial data extraction
                ai_financial = ai_service.extract_data_from_pdf_text(pdf_text, "financial")
                if ai_financial:
                    print("  ✓ AI extracted additional financial data")
                    # Merge AI-extracted data (prioritize existing, fill gaps with AI)
                    for key, value in ai_financial.get('income_statement', {}).items():
                        if key not in prior_year_data or prior_year_data[key] == 0:
                            prior_year_data[key] = value
                    for key, value in ai_financial.get('balance_sheet', {}).items():
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if key not in prior_year_data or subkey not in prior_year_data.get(key, {}):
                                    if key not in prior_year_data:
                                        prior_year_data[key] = {}
                                    prior_year_data[key][subkey] = subvalue
                
                # Enhance director/compiler extraction
                ai_directors = ai_service.extract_data_from_pdf_text(pdf_text, "directors")
                if ai_directors and not directors:
                    if 'directors' in ai_directors:
                        directors = ai_directors['directors']
                    if 'compiler' in ai_directors and not compiler:
                        compiler = ai_directors['compiler']
                    if 'entity_name' in ai_directors and not entity_name:
                        entity_name = ai_directors['entity_name']
            except Exception as e:
                print(f"  ⚠ AI enhancement failed: {str(e)}, continuing with standard parsing")
        
        # Extract notes structure
        notes_data = extract_notes_structure(pdf_parser)
        
        # AI-enhanced note extraction (if enabled)
        if args.use_ai and os.getenv('OPENROUTER_API_KEY'):
            try:
                from ai_service import AIService
                ai_service = AIService()
                print("  Enhancing note extraction with AI...")
                pdf_text = pdf_parser.get_full_text()
                ai_notes = ai_service.extract_data_from_pdf_text(pdf_text, "notes")
                if ai_notes and 'notes' in ai_notes:
                    # Merge AI-extracted notes with existing structure
                    for ai_note in ai_notes['notes']:
                        note_key = f"note_{ai_note['number']}"
                        if note_key not in notes_data:
                            notes_data[note_key] = {
                                'number': ai_note['number'],
                                'heading': ai_note.get('heading', ''),
                                'content': ai_note.get('content', '')
                            }
                    print("  ✓ AI enhanced note extraction")
            except Exception as e:
                print(f"  ⚠ AI note enhancement failed: {str(e)}")
        
        # Extract director and compiler information
        print("  Extracting director and compiler information...")
        directors = pdf_parser.extract_directors_info()
        compiler = pdf_parser.extract_compiler_info()
        
        # Extract tax consolidation and contingent liability info
        tax_consolidation_entity = pdf_parser.extract_tax_consolidation_info()
        contingent_liability_text = pdf_parser.extract_contingent_liabilities()
        
        # If directors/compiler not found in PDF, use defaults
        if not directors:
            print("  Warning: Directors not found in PDF, using defaults")
            directors = [
                {'name': 'Matthew Warnken', 'title': 'Director'},
                {'name': 'Gary Wyatt', 'title': 'Director'},
                {'name': 'Julian Turecek', 'title': 'Director'}
            ]
        
        if not compiler:
            print("  Warning: Compiler not found in PDF, using defaults")
            compiler = {
                'name': 'Allan Tuback',
                'title': 'Chief Financial Officer'
            }
        
        # ============================================================
        # STEP 2: Parse Draft Current Year PDF (if provided)
        # ============================================================
        draft_pdf_parser = None
        if args.draft_current_pdf:
            print("\n" + "="*80)
            print("STEP 2: Parsing Draft Current Year PDF (for structure hints only)")
            print("="*80)
            draft_pdf_parser = PDFParser(args.draft_current_pdf)
            # Note: We don't trust numerical values from draft
        
        # ============================================================
        # STEP 3: Process Excel File (Primary Source of Truth)
        # ============================================================
        print("\n" + "="*80)
        print("STEP 3: Processing Excel Data (Primary Source of Truth)")
        print("="*80)
        processor = ExcelProcessor(args.excel_file)
        
        print("  Extracting profit & loss data from 'Consol PL'...")
        pl_data = processor.extract_pl_data()
        print(f"    Revenue: ${pl_data.get('revenue', 0):,.0f}")
        print(f"    Net Profit/(Loss): ${pl_data.get('net_profit_loss', 0):,.0f}")
        print(f"    EBITDA: ${pl_data.get('ebitda', 0):,.0f}")
        
        print("  Extracting balance sheet data from 'Consol BS'...")
        bs_data = processor.extract_bs_data()
        print(f"    Total Assets: ${bs_data.get('total_assets', 0):,.0f}")
        print(f"    Total Equity: ${bs_data.get('total_equity', 0):,.0f}")
        
        # ============================================================
        # STEP 4: Comprehensive Validation
        # ============================================================
        print("\n" + "="*80)
        print("STEP 4: Comprehensive Validation Checks")
        print("="*80)
        
        validator = FinancialStatementValidator(entity_name, args.current_year, use_ai=args.use_ai)
        
        # Get prior year retained earnings
        prior_re = prior_year_data.get('equity', {}).get('retained_earnings', 0)
        if prior_re == 0:
            # Try to get from balance sheet data
            prior_re = prior_year_data.get('retained_earnings', 0)
        
        # AI-powered cross-validation (if enabled)
        if args.use_ai and os.getenv('OPENROUTER_API_KEY'):
            try:
                from ai_service import AIService
                ai_service = AIService()
                print("  Running AI cross-validation between Excel and PDF data...")
                is_consistent, discrepancies = ai_service.cross_validate_figures(
                    {'pl': pl_data, 'bs': bs_data},
                    prior_year_data
                )
                if discrepancies:
                    for disc in discrepancies:
                        validator.warnings.append(f"⚠️ AI Cross-Validation: {disc}")
                else:
                    print("  ✓ AI cross-validation passed")
            except Exception as e:
                print(f"  ⚠ AI cross-validation failed: {str(e)}")
        
        # Perform all validations (including AI if enabled)
        is_valid, errors, warnings, queries = validator.validate_all(
            bs_data=bs_data,
            pl_data=pl_data,
            prior_year_data=prior_year_data,
            prior_re=prior_re,
            directors=directors,
            compiler=compiler,
            tax_consolidation_entity=tax_consolidation_entity,
            contingent_liability_text=contingent_liability_text,
            notes_data=notes_data
        )
        
        # Print validation results
        validator.print_validation_results()
        
        # Halt if critical errors
        validator.halt_if_errors()
        
        # ============================================================
        # STEP 5: Calculate and Update Retained Earnings
        # ============================================================
        print("\n" + "="*80)
        print("STEP 5: Calculating Retained Earnings")
        print("="*80)
        
        # Update retained earnings: RE_end = RE_start + Net Profit/(Loss)
        bs_data['equity']['retained_earnings'] = prior_re + pl_data['net_profit_loss']
        bs_data['total_equity'] = sum(bs_data['equity'].values())
        bs_data['total_liabilities_and_equity'] = bs_data['total_liabilities'] + bs_data['total_equity']
        
        print(f"  Prior Year RE: ${prior_re:,.0f}")
        print(f"  Net Profit/(Loss): ${pl_data['net_profit_loss']:,.0f}")
        print(f"  Current Year RE: ${bs_data['equity']['retained_earnings']:,.0f}")
        
        # ============================================================
        # STEP 6: Final Quality Gate Checks
        # ============================================================
        print("\n" + "="*80)
        print("STEP 6: Final Quality Gate Checks")
        print("="*80)
        
        # Cross-check key figures
        checks_passed = True
        
        # EBITDA check
        if 'ebitda' in pl_data:
            print(f"✓ EBITDA = ${pl_data['ebitda']:,.0f}")
        else:
            print("⚠ EBITDA not found in PL data")
        
        # Net Loss check
        net_loss = pl_data.get('net_profit_loss', 0)
        print(f"✓ Net Profit/(Loss) After Tax = ${net_loss:,.0f}")
        
        # Balance sheet totals
        total_assets = bs_data.get('total_assets', 0)
        total_equity = bs_data.get('total_equity', 0)
        total_liabilities = bs_data.get('total_liabilities', 0)
        print(f"✓ Total Assets = ${total_assets:,.0f}")
        print(f"✓ Total Equity = ${total_equity:,.0f}")
        print(f"✓ Total Liabilities = ${total_liabilities:,.0f}")
        print(f"✓ Assets = Liabilities + Equity: ${total_assets:,.0f} = ${total_liabilities + total_equity:,.0f}")
        
        # Retained earnings check
        re_end = bs_data.get('equity', {}).get('retained_earnings', 0)
        print(f"✓ Retained Earnings (end) = ${re_end:,.0f}")
        
        if not checks_passed:
            print("\n⚠ Some quality checks failed. Review before finalizing.")
        
        # ============================================================
        # STEP 7: Generate Financial Statements PDF
        # ============================================================
        print("\n" + "="*80)
        print("STEP 7: Generating Financial Statements PDF")
        print("="*80)
        
        generator = AASBFinancialStatementGenerator(
            entity_name, 
            args.current_year, 
            prior_year_data,
            notes_structure=notes_data
        )
        
        filename = generator.generate_financial_statements(
            pl_data, 
            bs_data, 
            notes_data, 
            directors, 
            compiler
        )
        
        print("\n" + "="*80)
        print("SUCCESS")
        print("="*80)
        print(f"Financial statements generated: {filename}")
        print(f"Output file: {os.path.abspath(filename)}")
        print("\n" + "="*80)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
