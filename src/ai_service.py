"""
AI-powered service for financial statement validation and enhancement.
Uses OpenRouter API with multiple models for different tasks.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum


class AIModel(Enum):
    """Available AI models for different tasks."""
    GROK_FAST = "x-ai/grok-4.1-fast"  # Best for reasoning and complex tasks
    GEMINI_FLASH = "google/gemini-2.5-flash-lite"  # Fast, cost-effective
    GPT_NANO = "openai/gpt-4.1-nano"  # General purpose
    GPT_MINI = "openai/gpt-5-mini"  # Fallback if reasoning fails
    NEMOTRON_VL = "nvidia/nemotron-nano-12b-v2-vl"  # Document intelligence, OCR, charts


class AIService:
    """
    AI service for financial statement validation and enhancement.
    Uses OpenRouter API with model selection based on task type.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI service.
        
        Args:
            api_key: OpenRouter API key. If None, reads from OPENROUTER_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key required. Set OPENROUTER_API_KEY environment variable.")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Optional
            "X-Title": "AASB Financial Statement Generator"  # Optional
        }
    
    def _call_api(self, model: AIModel, messages: List[Dict[str, str]], 
                  reasoning_enabled: bool = False, temperature: float = 0.3) -> Dict[str, Any]:
        """
        Call OpenRouter API.
        
        Args:
            model: AI model to use
            messages: List of message dictionaries
            reasoning_enabled: Enable reasoning mode (for Grok)
            temperature: Sampling temperature
            
        Returns:
            API response dictionary
        """
        payload = {
            "model": model.value,
            "messages": messages,
            "temperature": temperature
        }
        
        # Enable reasoning for Grok if requested
        if model == AIModel.GROK_FAST and reasoning_enabled:
            payload["reasoning"] = True
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    def validate_balance_sheet_relationships(self, bs_data: Dict[str, Any], 
                                            pl_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Use AI to validate balance sheet relationships and identify issues.
        
        Args:
            bs_data: Balance sheet data
            pl_data: Profit & loss data
            
        Returns:
            Tuple of (is_valid, message, analysis)
        """
        prompt = f"""You are a financial statement validator for Australian AASB-compliant financial statements.

Analyze the following balance sheet and profit & loss data for consistency and accuracy:

BALANCE SHEET:
{json.dumps(bs_data, indent=2)}

PROFIT & LOSS:
{json.dumps(pl_data, indent=2)}

Please:
1. Verify Assets = Liabilities + Equity
2. Check retained earnings rollforward: RE_end should equal RE_start + Net Profit/(Loss)
3. Identify any unusual relationships or potential errors
4. Check for missing line items that should be present
5. Validate totals are correctly calculated

Respond in JSON format:
{{
    "is_valid": true/false,
    "issues": ["list of issues found"],
    "recommendations": ["list of recommendations"],
    "calculated_totals": {{
        "assets": calculated_value,
        "liabilities_equity": calculated_value,
        "difference": difference_value
    }},
    "retained_earnings_check": {{
        "prior_re": value,
        "net_profit_loss": value,
        "expected_re": value,
        "actual_re": value,
        "difference": value
    }}
}}"""

        messages = [
            {"role": "system", "content": "You are an expert financial statement validator specializing in AASB standards for Australian companies."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._call_api(AIModel.GROK_FAST, messages, reasoning_enabled=True)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON from response
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()
            
            analysis = json.loads(json_str)
            is_valid = analysis.get('is_valid', False)
            issues = analysis.get('issues', [])
            message = "\n".join(issues) if issues else "All checks passed"
            
            return is_valid, message, analysis
            
        except Exception as e:
            # Fallback to simpler model
            print(f"  Warning: AI validation failed ({str(e)}), using fallback model...")
            try:
                response = self._call_api(AIModel.GPT_MINI, messages)
                content = response['choices'][0]['message']['content']
                return True, "AI validation completed (fallback)", {"raw_response": content}
            except Exception as e2:
                return True, f"AI validation unavailable: {str(e2)}", {}
    
    def validate_note_disclosures(self, notes_data: Dict[str, Any], 
                                 bs_data: Dict[str, Any], 
                                 pl_data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Use AI to validate note disclosures are appropriate and complete.
        
        Args:
            notes_data: Notes structure and content
            bs_data: Balance sheet data
            pl_data: Profit & loss data
            
        Returns:
            Tuple of (is_complete, missing_disclosures, analysis)
        """
        prompt = f"""You are an AASB compliance expert for Australian non-reporting entities.

Review the financial statement notes and identify:
1. Missing required disclosures per AASB 101, 108, and 1048
2. Notes that should be present based on the financial data
3. Incomplete or inadequate disclosures
4. Notes that should be removed (if balances are zero and not required)

FINANCIAL DATA:
Balance Sheet: {json.dumps(bs_data, indent=2)}
Profit & Loss: {json.dumps(pl_data, indent=2)}

NOTES STRUCTURE:
{json.dumps(notes_data, indent=2)}

For non-reporting entities, required disclosures include:
- Note 1: Significant accounting policies (basis of preparation)
- Note 2: New accounting pronouncements
- Note 3: Income tax (especially if no tax recognized)
- Notes for material line items (PPE, receivables, payables, borrowings, etc.)

Respond in JSON format:
{{
    "is_complete": true/false,
    "missing_disclosures": ["list of missing required disclosures"],
    "inadequate_notes": ["list of notes needing more detail"],
    "unnecessary_notes": ["list of notes that can be removed"],
    "recommendations": ["specific recommendations for each note"]
}}"""

        messages = [
            {"role": "system", "content": "You are an AASB compliance expert specializing in non-reporting entity requirements."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._call_api(AIModel.GROK_FAST, messages, reasoning_enabled=True)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()
            
            analysis = json.loads(json_str)
            is_complete = analysis.get('is_complete', False)
            missing = analysis.get('missing_disclosures', [])
            
            return is_complete, missing, analysis
            
        except Exception as e:
            print(f"  Warning: AI note validation failed ({str(e)}), using fallback...")
            try:
                response = self._call_api(AIModel.GEMINI_FLASH, messages)
                content = response['choices'][0]['message']['content']
                return True, [], {"raw_response": content}
            except:
                return True, [], {}
    
    def extract_data_from_pdf_text(self, pdf_text: str, data_type: str = "financial") -> Dict[str, Any]:
        """
        Use AI (Nemotron VL for document intelligence) to extract structured data from PDF text.
        Useful for complex PDF layouts that standard parsing misses.
        
        Args:
            pdf_text: Extracted text from PDF
            data_type: Type of data to extract ("financial", "directors", "notes")
            
        Returns:
            Extracted structured data
        """
        if data_type == "financial":
            prompt = f"""Extract financial statement data from the following PDF text.

Extract:
1. Income Statement items (Revenue, Expenses, Profit/Loss)
2. Balance Sheet items (Assets, Liabilities, Equity)
3. All amounts in AUD (rounded to nearest dollar)
4. Prior year comparatives

PDF TEXT:
{pdf_text[:8000]}  # Limit text length

Respond in JSON format with this structure:
{{
    "income_statement": {{
        "revenue": value,
        "cost_of_sales": value,
        "gross_profit": value,
        "other_income": value,
        "distribution_costs": value,
        "administrative_expenses": value,
        "other_expenses": value,
        "profit_before_tax": value,
        "income_tax_expense": value,
        "net_profit_loss": value
    }},
    "balance_sheet": {{
        "current_assets": {{"cash": value, "receivables": value, "inventories": value, "other": value}},
        "non_current_assets": {{"ppe": value, "intangibles": value, "other": value}},
        "current_liabilities": {{"payables": value, "provisions": value, "other": value}},
        "non_current_liabilities": {{"borrowings": value, "provisions": value, "other": value}},
        "equity": {{"share_capital": value, "reserves": value, "retained_earnings": value}}
    }}
}}"""
        elif data_type == "directors":
            prompt = f"""Extract director and compiler information from the following PDF text.

Look for:
1. Director names and titles from Directors' Declaration
2. Compilation signatory name and title
3. Entity name

PDF TEXT:
{pdf_text[:4000]}

Respond in JSON:
{{
    "entity_name": "name",
    "directors": [{{"name": "name", "title": "title"}}],
    "compiler": {{"name": "name", "title": "title"}}
}}"""
        else:  # notes
            prompt = f"""Extract notes structure from the following PDF text.

Identify:
1. Note numbers and headings
2. Note content (first paragraph of each note)

PDF TEXT:
{pdf_text[:6000]}

Respond in JSON:
{{
    "notes": [
        {{"number": 1, "heading": "heading", "content": "first paragraph"}},
        ...
    ]
}}"""

        messages = [
            {"role": "system", "content": "You are an expert at extracting structured financial data from PDF documents."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Use Nemotron for document intelligence
            response = self._call_api(AIModel.NEMOTRON_VL, messages, temperature=0.1)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"  Warning: AI extraction failed ({str(e)}), falling back to standard parsing")
            return {}
    
    def cross_validate_figures(self, excel_data: Dict[str, Any], 
                              pdf_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Use AI to cross-validate figures between Excel and PDF sources.
        
        Args:
            excel_data: Data extracted from Excel
            pdf_data: Data extracted from PDF
            
        Returns:
            Tuple of (is_consistent, discrepancies)
        """
        prompt = f"""Compare financial data from two sources (Excel and PDF) and identify discrepancies.

EXCEL DATA (Source of Truth for Current Year):
{json.dumps(excel_data, indent=2)}

PDF DATA (Prior Year Comparatives):
{json.dumps(pdf_data, indent=2)}

Identify:
1. Significant discrepancies between sources
2. Missing data in either source
3. Calculation errors
4. Formatting inconsistencies

Note: Excel is the source of truth for current year figures.
PDF should only be used for prior year comparatives.

Respond in JSON:
{{
    "is_consistent": true/false,
    "discrepancies": ["list of discrepancies"],
    "recommendations": ["recommendations to resolve"]
}}"""

        messages = [
            {"role": "system", "content": "You are a financial data validation expert."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._call_api(AIModel.GEMINI_FLASH, messages)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()
            
            analysis = json.loads(json_str)
            is_consistent = analysis.get('is_consistent', True)
            discrepancies = analysis.get('discrepancies', [])
            
            return is_consistent, discrepancies
            
        except Exception as e:
            print(f"  Warning: AI cross-validation failed ({str(e)})")
            return True, []
    
    def generate_note_content(self, note_number: int, note_heading: str, 
                            financial_data: Dict[str, Any]) -> str:
        """
        Use AI to generate appropriate note content based on financial data.
        
        Args:
            note_number: Note number
            note_heading: Note heading
            financial_data: Relevant financial data for the note
            
        Returns:
            Generated note content
        """
        prompt = f"""Generate AASB-compliant note content for a non-reporting entity financial statement.

Note {note_number}: {note_heading}

Financial Data:
{json.dumps(financial_data, indent=2)}

Requirements:
1. AASB-compliant for non-reporting entities
2. Appropriate level of detail (not exhaustive)
3. Professional, clear language
4. Include prior year comparatives if relevant
5. Follow Australian accounting terminology

Generate the note content (2-4 paragraphs typically)."""

        messages = [
            {"role": "system", "content": "You are an expert at writing AASB-compliant financial statement notes for Australian non-reporting entities."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._call_api(AIModel.GPT_NANO, messages, temperature=0.4)
            content = response['choices'][0]['message']['content']
            return content.strip()
            
        except Exception as e:
            print(f"  Warning: AI note generation failed ({str(e)})")
            return f"Note {note_number}: {note_heading} - [Content to be added]"
    
    def validate_tax_consolidation_disclosure(self, note_content: str, 
                                              head_entity_name: str) -> Tuple[bool, str]:
        """
        Use AI to validate tax consolidation disclosure is correct.
        
        Args:
            note_content: Note 3 content
            head_entity_name: Expected head entity name
            
        Returns:
            Tuple of (is_correct, message)
        """
        prompt = f"""Validate that the tax consolidation disclosure correctly references the head entity.

Note Content:
{note_content}

Expected Head Entity: {head_entity_name}

Check:
1. Head entity name is correctly stated
2. Disclosure follows AASB requirements
3. Wording is consistent with prior year (if applicable)

Respond in JSON:
{{
    "is_correct": true/false,
    "head_entity_found": true/false,
    "head_entity_name_in_note": "name found or null",
    "issues": ["list of issues"],
    "recommendation": "recommended action"
}}"""

        messages = [
            {"role": "system", "content": "You are an expert in Australian tax consolidation disclosure requirements."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._call_api(AIModel.GEMINI_FLASH, messages)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()
            
            analysis = json.loads(json_str)
            is_correct = analysis.get('is_correct', False)
            message = analysis.get('recommendation', '')
            
            return is_correct, message
            
        except Exception as e:
            print(f"  Warning: AI tax validation failed ({str(e)})")
            return True, "Validation unavailable"

