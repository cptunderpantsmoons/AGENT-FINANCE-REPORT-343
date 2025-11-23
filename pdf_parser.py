"""
PDF Parser for extracting structure, wording, and data from prior-year financial statements.
"""

import re
import pdfplumber
from typing import Dict, Any, List, Optional, Tuple
from collections import OrderedDict


class PDFParser:
    """
    Parses prior-year financial statement PDFs to extract:
    - Structure and section order
    - Note headings and numbering
    - Accounting policy wording
    - Prior-year comparative figures
    - Director names and titles
    - Compilation signatory information
    """
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF parser.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.text_content = []
        self.pages = []
        self._load_pdf()
    
    def _load_pdf(self):
        """Load and extract text from PDF."""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        self.text_content.append(text)
                        self.pages.append(page)
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")
    
    def extract_entity_name(self) -> Optional[str]:
        """Extract entity name from title page."""
        if not self.text_content:
            return None
        
        # Look for "Financial Statements" followed by entity name
        first_page = self.text_content[0]
        lines = first_page.split('\n')
        
        for i, line in enumerate(lines):
            if 'Financial Statements' in line and i + 1 < len(lines):
                # Next line is likely the entity name
                entity_name = lines[i + 1].strip()
                if entity_name and entity_name != 'For the Year Ended':
                    return entity_name
        
        return None
    
    def extract_prior_year(self) -> Optional[int]:
        """Extract prior year from PDF."""
        if not self.text_content:
            return None
        
        # Look for "For the Year Ended 30 June YYYY"
        pattern = r'For the Year Ended 30 June (\d{4})'
        for page_text in self.text_content:
            match = re.search(pattern, page_text)
            if match:
                return int(match.group(1))
        
        return None
    
    def extract_section_structure(self) -> Dict[str, int]:
        """
        Extract section structure and page numbers from contents page.
        
        Returns:
            Dict[str, int]: Section names mapped to page numbers
        """
        sections = OrderedDict()
        
        if not self.text_content:
            return sections
        
        # Look for Contents page
        contents_pattern = r'Contents|CONTENTS'
        for page_idx, page_text in enumerate(self.text_content):
            if re.search(contents_pattern, page_text, re.IGNORECASE):
                # Extract section names and page numbers
                lines = page_text.split('\n')
                in_contents = False
                
                for line in lines:
                    if re.search(contents_pattern, line, re.IGNORECASE):
                        in_contents = True
                        continue
                    
                    if in_contents:
                        # Look for numbered sections (e.g., "1. Statement of...")
                        match = re.match(r'(\d+)\.\s+(.+?)(?:\s+(\d+))?$', line.strip())
                        if match:
                            section_num = match.group(1)
                            section_name = match.group(2).strip()
                            page_num = match.group(3)
                            if page_num:
                                sections[section_name] = int(page_num)
                            else:
                                # Try to find page number in next part of line
                                parts = line.split()
                                for part in reversed(parts):
                                    if part.isdigit():
                                        sections[section_name] = int(part)
                                        break
        
        return sections
    
    def extract_income_statement_data(self) -> Dict[str, Any]:
        """
        Extract income statement data from prior year.
        
        Returns:
            Dict[str, Any]: Income statement line items with prior-year values
        """
        data = {}
        
        if not self.text_content:
            return data
        
        # Look for income statement section
        income_statement_pattern = r'Statement of Profit or Loss|Income Statement|Profit and Loss'
        
        for page_text in self.text_content:
            if re.search(income_statement_pattern, page_text, re.IGNORECASE):
                lines = page_text.split('\n')
                
                # Extract line items
                for line in lines:
                    # Revenue
                    if re.search(r'^Revenue\s+', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['revenue'] = value
                    
                    # Cost of Sales
                    elif re.search(r'Cost of Sales|Cost of Goods Sold', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['cost_of_sales'] = abs(value)
                    
                    # Gross Profit
                    elif re.search(r'Gross Profit', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['gross_profit'] = value
                    
                    # Other Income
                    elif re.search(r'Other Income', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['other_income'] = value
                    
                    # Distribution Costs
                    elif re.search(r'Distribution Costs?', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['distribution_costs'] = abs(value)
                    
                    # Administrative Expenses
                    elif re.search(r'Administrative Expenses?', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['administrative_expenses'] = abs(value)
                    
                    # Other Expenses
                    elif re.search(r'Other Expenses?', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['other_expenses'] = abs(value)
                    
                    # Profit Before Tax
                    elif re.search(r'Profit Before Tax', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['profit_before_tax'] = value
                    
                    # Income Tax Expense
                    elif re.search(r'Income Tax Expense', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['income_tax_expense'] = abs(value)
                    
                    # Net Profit/(Loss)
                    elif re.search(r'Profit.*Loss.*Period|Net Profit|Net Loss', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['net_profit_loss'] = value
        
        return data
    
    def extract_balance_sheet_data(self) -> Dict[str, Any]:
        """
        Extract balance sheet data from prior year.
        
        Returns:
            Dict[str, Any]: Balance sheet line items with prior-year values
        """
        data = {
            'current_assets': {},
            'non_current_assets': {},
            'current_liabilities': {},
            'non_current_liabilities': {},
            'equity': {}
        }
        
        if not self.text_content:
            return data
        
        # Look for balance sheet section
        bs_pattern = r'Statement of Financial Position|Balance Sheet'
        
        for page_text in self.text_content:
            if re.search(bs_pattern, page_text, re.IGNORECASE):
                lines = page_text.split('\n')
                
                # Extract line items
                for line in lines:
                    # Cash
                    if re.search(r'Cash.*Equivalent', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['current_assets']['cash'] = value
                    
                    # Receivables
                    elif re.search(r'Trade.*Receivable|Receivables', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['current_assets']['receivables'] = value
                    
                    # Inventories
                    elif re.search(r'Inventor', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['current_assets']['inventories'] = value
                    
                    # PPE
                    elif re.search(r'Property.*Plant.*Equipment|PPE', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['non_current_assets']['ppe'] = value
                    
                    # Intangibles
                    elif re.search(r'Intangible', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['non_current_assets']['intangibles'] = value
                    
                    # Payables
                    elif re.search(r'Trade.*Payable|Payables', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['current_liabilities']['payables'] = value
                    
                    # Borrowings
                    elif re.search(r'Borrowing', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['non_current_liabilities']['borrowings'] = value
                    
                    # Share Capital
                    elif re.search(r'Share Capital', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['equity']['share_capital'] = value
                    
                    # Retained Earnings
                    elif re.search(r'Retained Earnings', line, re.IGNORECASE):
                        value = self._extract_currency_value(line)
                        if value is not None:
                            data['equity']['retained_earnings'] = value
        
        # Calculate totals
        data['total_current_assets'] = sum(data['current_assets'].values())
        data['total_non_current_assets'] = sum(data['non_current_assets'].values())
        data['total_assets'] = data['total_current_assets'] + data['total_non_current_assets']
        
        data['total_current_liabilities'] = sum(data['current_liabilities'].values())
        data['total_non_current_liabilities'] = sum(data['non_current_liabilities'].values())
        data['total_liabilities'] = data['total_current_liabilities'] + data['total_non_current_liabilities']
        
        data['total_equity'] = sum(data['equity'].values())
        data['total_liabilities_and_equity'] = data['total_liabilities'] + data['total_equity']
        
        return data
    
    def extract_notes_structure(self) -> List[Dict[str, Any]]:
        """
        Extract note structure and headings from prior year.
        
        Returns:
            List[Dict[str, Any]]: List of note dictionaries with headings and content
        """
        notes = []
        
        if not self.text_content:
            return notes
        
        # Look for Notes section
        notes_pattern = r'Notes to the Financial Statements|NOTES'
        
        in_notes = False
        current_note = None
        
        for page_text in self.text_content:
            lines = page_text.split('\n')
            
            for line in lines:
                # Check if we're entering notes section
                if re.search(notes_pattern, line, re.IGNORECASE):
                    in_notes = True
                    continue
                
                if in_notes:
                    # Look for note headings (e.g., "1. Significant accounting policies")
                    match = re.match(r'(\d+)\.\s+(.+?)(?:\s|$)', line.strip())
                    if match:
                        # Save previous note if exists
                        if current_note:
                            notes.append(current_note)
                        
                        note_num = int(match.group(1))
                        note_heading = match.group(2).strip()
                        current_note = {
                            'number': note_num,
                            'heading': note_heading,
                            'content': []
                        }
                    elif current_note:
                        # Add content to current note
                        if line.strip():
                            current_note['content'].append(line.strip())
        
        # Add last note
        if current_note:
            notes.append(current_note)
        
        return notes
    
    def extract_directors_info(self) -> List[Dict[str, str]]:
        """
        Extract director names and titles from directors' declaration.
        
        Returns:
            List[Dict[str, str]]: List of director dictionaries
        """
        directors = []
        
        if not self.text_content:
            return directors
        
        # Look for Directors' Declaration
        declaration_pattern = r"Directors' Declaration|DIRECTORS' DECLARATION"
        
        in_declaration = False
        
        for page_text in self.text_content:
            lines = page_text.split('\n')
            
            for i, line in enumerate(lines):
                if re.search(declaration_pattern, line, re.IGNORECASE):
                    in_declaration = True
                    continue
                
                if in_declaration:
                    # Look for signature lines
                    # Pattern: Name on one line, Title on next line
                    if i + 2 < len(lines):
                        name_line = lines[i].strip()
                        title_line = lines[i + 1].strip()
                        
                        # Check if this looks like a director entry
                        if name_line and title_line and 'Director' in title_line:
                            # Remove date/underscore markers
                            name = re.sub(r'[_\d\s]+Date.*', '', name_line).strip()
                            if name and len(name) > 3:  # Valid name
                                directors.append({
                                    'name': name,
                                    'title': title_line
                                })
        
        return directors
    
    def extract_compiler_info(self) -> Optional[Dict[str, str]]:
        """
        Extract compilation signatory information.
        
        Returns:
            Optional[Dict[str, str]]: Compiler information or None
        """
        if not self.text_content:
            return None
        
        # Look for Compilation Report
        compilation_pattern = r'Compilation Report|Independent Compilation'
        
        for page_text in self.text_content:
            if re.search(compilation_pattern, page_text, re.IGNORECASE):
                lines = page_text.split('\n')
                
                for i, line in enumerate(lines):
                    # Look for name and title after signature line
                    if '_____' in line or 'Date:' in line:
                        if i + 2 < len(lines):
                            name = lines[i + 1].strip()
                            title = lines[i + 2].strip()
                            
                            if name and title:
                                return {
                                    'name': name,
                                    'title': title
                                }
        
        return None
    
    def extract_tax_consolidation_info(self) -> Optional[str]:
        """
        Extract tax consolidation head entity name from Note 3(b)(i).
        
        Returns:
            Optional[str]: Head entity name or None
        """
        if not self.text_content:
            return None
        
        # Look for Note 3 and tax consolidation section
        for page_text in self.text_content:
            if 'Note 3' in page_text or '3.' in page_text:
                # Look for tax consolidation or head entity
                match = re.search(r'head entity[:\s]+([A-Za-z\s]+(?:Pty|Ltd|Limited))', page_text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return None
    
    def extract_contingent_liabilities(self) -> Optional[str]:
        """
        Extract contingent liability wording (e.g., TENBS) from notes.
        
        Returns:
            Optional[str]: Contingent liability text or None
        """
        if not self.text_content:
            return None
        
        # Look for contingent liabilities or commitments
        for page_text in self.text_content:
            if 'contingent' in page_text.lower() or 'TENBS' in page_text:
                # Extract relevant paragraph
                lines = page_text.split('\n')
                for i, line in enumerate(lines):
                    if 'contingent' in line.lower() or 'TENBS' in line:
                        # Get surrounding context
                        context = '\n'.join(lines[max(0, i-2):min(len(lines), i+5)])
                        return context.strip()
        
        return None
    
    def _extract_currency_value(self, text: str) -> Optional[float]:
        """
        Extract currency value from text line.
        
        Args:
            text (str): Text line containing currency value
            
        Returns:
            Optional[float]: Extracted value or None
        """
        # Look for currency patterns: $123,456 or (123,456) or -123,456
        patterns = [
            r'\$([\d,]+)',
            r'\(([\d,]+)\)',  # Negative in parentheses
            r'-?\$?([\d,]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Take the last match (usually the current year value)
                value_str = matches[-1].replace(',', '')
                try:
                    value = float(value_str)
                    # Check if it's negative (parentheses or minus sign)
                    if '(' in text or text.strip().startswith('-'):
                        return -value
                    return value
                except ValueError:
                    continue
        
        return None
    
    def get_full_text(self) -> str:
        """Get full text content of PDF."""
        return '\n\n'.join(self.text_content)

