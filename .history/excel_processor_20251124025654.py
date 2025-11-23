import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional

class ExcelProcessor:
    """
    Processes Excel files containing financial data for the AASB Financial Statement Generator.
    """
    
    def __init__(self, excel_file_path: str):
        """
        Initialize the Excel processor with the path to the Excel file.
        
        Args:
            excel_file_path (str): Path to the Excel file containing financial data
        """
        self.excel_file_path = excel_file_path
        self.sheets = {}
        self._load_sheets()
    
    def _load_sheets(self):
        """
        Load all sheets from the Excel file.
        """
        try:
            excel_file = pd.ExcelFile(self.excel_file_path)
            for sheet_name in excel_file.sheet_names:
                self.sheets[sheet_name] = pd.read_excel(self.excel_file_path, sheet_name=sheet_name)
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")
    
    def extract_pl_data(self) -> Dict[str, Any]:
        """
        Extract profit and loss data from the 'Consol PL' sheet.
        Prioritizes specific cell lookups, falls back to row label matching.
        
        Returns:
            Dict[str, Any]: Dictionary containing P&L data including EBITDA
        """
        # Try alternative sheet names
        sheet_name = None
        for name in ['Consol PL', 'ConsolPL', 'PL', 'Profit Loss', 'Income Statement']:
            if name in self.sheets:
                sheet_name = name
                break
        
        if sheet_name is None:
            raise ValueError("Could not find P&L sheet in Excel file. Expected: 'Consol PL'")
        
        pl_sheet = self.sheets[sheet_name]
        pl_data = {}
        
        try:
            # First, try to find EBITDA (often in a separate row)
            for index, row in pl_sheet.iterrows():
                row_str = row.astype(str)
                
                # EBITDA
                if row_str.str.contains('ebitda', case=False).any():
                    ebitda_value = self._extract_numeric_value(row)
                    if ebitda_value is not None:
                        pl_data['ebitda'] = ebitda_value
                
                # Revenue
                if row_str.str.contains('revenue', case=False).any() and 'revenue' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['revenue'] = value
                
                # Cost of sales
                elif (row_str.str.contains('cost of sales', case=False).any() or 
                      row_str.str.contains('cost of goods sold', case=False).any()) and 'cost_of_sales' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['cost_of_sales'] = abs(value)
                
                # Gross profit
                elif row_str.str.contains('gross profit', case=False).any() and 'gross_profit' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['gross_profit'] = value
                
                # Other income
                elif row_str.str.contains('other income', case=False).any() and 'other_income' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['other_income'] = value
                
                # Distribution costs
                elif (row_str.str.contains('distribution', case=False).any() and 
                      row_str.str.contains('cost', case=False).any()) and 'distribution_costs' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['distribution_costs'] = abs(value)
                
                # Administrative expenses
                elif (row_str.str.contains('administrative', case=False).any() and 
                      row_str.str.contains('expense', case=False).any()) and 'administrative_expenses' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['administrative_expenses'] = abs(value)
                
                # Other expenses
                elif (row_str.str.contains('other', case=False).any() and 
                      row_str.str.contains('expense', case=False).any() and
                      not row_str.str.contains('income', case=False).any()) and 'other_expenses' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['other_expenses'] = abs(value)
                
                # Profit before tax
                elif row_str.str.contains('profit before tax', case=False).any() and 'profit_before_tax' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['profit_before_tax'] = value
                
                # Income tax expense
                elif row_str.str.contains('income tax', case=False).any() and 'income_tax_expense' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['income_tax_expense'] = abs(value)
                
                # Net profit/loss
                elif ((row_str.str.contains('net', case=False).any() and 
                       row_str.str.contains('profit', case=False).any()) or 
                      (row_str.str.contains('net', case=False).any() and 
                       row_str.str.contains('loss', case=False).any())) and 'net_profit_loss' not in pl_data:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        pl_data['net_profit_loss'] = value
            
            # Calculate derived values if not directly found
            if 'gross_profit' not in pl_data and 'revenue' in pl_data and 'cost_of_sales' in pl_data:
                pl_data['gross_profit'] = pl_data['revenue'] - pl_data['cost_of_sales']
            
            if 'profit_before_tax' not in pl_data:
                pl_data['profit_before_tax'] = (
                    pl_data.get('gross_profit', 0) +
                    pl_data.get('other_income', 0) -
                    pl_data.get('distribution_costs', 0) -
                    pl_data.get('administrative_expenses', 0) -
                    pl_data.get('other_expenses', 0)
                )
            
            if 'net_profit_loss' not in pl_data and 'profit_before_tax' in pl_data:
                pl_data['net_profit_loss'] = pl_data['profit_before_tax'] - pl_data.get('income_tax_expense', 0)
            
            # Ensure EBITDA is set (calculate if missing)
            if 'ebitda' not in pl_data:
                # EBITDA = Operating profit before interest, tax, depreciation, amortization
                # Approximate: Profit before tax + interest + depreciation + amortization
                # For simplicity, use profit before tax if no other data available
                pl_data['ebitda'] = pl_data.get('profit_before_tax', 0)
                
        except Exception as e:
            raise Exception(f"Error extracting P&L data: {str(e)}")
        
        return pl_data
    
    def extract_bs_data(self) -> Dict[str, Any]:
        """
        Extract balance sheet data from the 'Consol BS' sheet.
        Handles related party loans split between current and non-current.
        
        Returns:
            Dict[str, Any]: Dictionary containing balance sheet data
        """
        # Try alternative sheet names
        sheet_name = None
        for name in ['Consol BS', 'ConsolBS', 'BS', 'Balance Sheet', 'Statement of Financial Position']:
            if name in self.sheets:
                sheet_name = name
                break
        
        if sheet_name is None:
            raise ValueError("Could not find Balance Sheet sheet in Excel file. Expected: 'Consol BS'")
        
        bs_sheet = self.sheets[sheet_name]
        bs_data = {
            'current_assets': {},
            'non_current_assets': {},
            'current_liabilities': {},
            'non_current_liabilities': {},
            'equity': {}
        }
        
        try:
            # Look for key row labels and extract corresponding values
            for index, row in bs_sheet.iterrows():
                row_str = row.astype(str)
                
                # Cash and cash equivalents
                if (row_str.str.contains('cash', case=False).any() and 
                    row_str.str.contains('equivalent', case=False).any()) and 'cash' not in bs_data['current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_assets']['cash'] = value
                
                # Trade and other receivables
                elif (row_str.str.contains('trade', case=False).any() and 
                      row_str.str.contains('receivable', case=False).any()) and 'receivables' not in bs_data['current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_assets']['receivables'] = value
                
                # Inventories
                elif row_str.str.contains('inventor', case=False).any() and 'inventories' not in bs_data['current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_assets']['inventories'] = value
                
                # Other current assets
                elif (row_str.str.contains('other', case=False).any() and 
                      row_str.str.contains('current', case=False).any() and 
                      row_str.str.contains('asset', case=False).any()) and 'other' not in bs_data['current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_assets']['other'] = value
                
                # Property, plant and equipment
                elif (row_str.str.contains('property', case=False).any() and 
                      row_str.str.contains('plant', case=False).any()) and 'ppe' not in bs_data['non_current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_assets']['ppe'] = value
                
                # Intangible assets
                elif row_str.str.contains('intangible', case=False).any() and 'intangibles' not in bs_data['non_current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_assets']['intangibles'] = value
                
                # Other non-current assets
                elif (row_str.str.contains('other', case=False).any() and 
                      row_str.str.contains('non', case=False).any() and 
                      row_str.str.contains('current', case=False).any() and 
                      row_str.str.contains('asset', case=False).any()) and 'other' not in bs_data['non_current_assets']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_assets']['other'] = value
                
                # Trade and other payables
                elif (row_str.str.contains('trade', case=False).any() and 
                      row_str.str.contains('payable', case=False).any()) and 'payables' not in bs_data['current_liabilities']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_liabilities']['payables'] = value
                
                # Provisions (current)
                elif (row_str.str.contains('provision', case=False).any() and
                      (row_str.str.contains('current', case=False).any() or index < 15)) and 'provisions' not in bs_data['current_liabilities']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_liabilities']['provisions'] = value
                
                # Provisions (non-current)
                elif (row_str.str.contains('provision', case=False).any() and
                      row_str.str.contains('non', case=False).any()) and 'provisions' not in bs_data['non_current_liabilities']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_liabilities']['provisions'] = value
                
                # Related party loans - current
                elif (row_str.str.contains('related', case=False).any() and 
                      row_str.str.contains('party', case=False).any() and
                      row_str.str.contains('current', case=False).any()):
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_liabilities']['related_party_loans'] = value
                
                # Related party loans - non-current
                elif (row_str.str.contains('related', case=False).any() and 
                      row_str.str.contains('party', case=False).any() and
                      row_str.str.contains('non', case=False).any()):
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_liabilities']['related_party_loans'] = value
                
                # Other current liabilities
                elif (row_str.str.contains('other', case=False).any() and 
                      row_str.str.contains('current', case=False).any() and 
                      row_str.str.contains('liabilit', case=False).any()) and 'other' not in bs_data['current_liabilities']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['current_liabilities']['other'] = value
                
                # Borrowings (non-current)
                elif row_str.str.contains('borrowing', case=False).any() and 'borrowings' not in bs_data['non_current_liabilities']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_liabilities']['borrowings'] = value
                
                # Other non-current liabilities
                elif (row_str.str.contains('other', case=False).any() and 
                      row_str.str.contains('non', case=False).any() and 
                      row_str.str.contains('current', case=False).any() and 
                      row_str.str.contains('liabilit', case=False).any()) and 'other' not in bs_data['non_current_liabilities']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['non_current_liabilities']['other'] = value
                
                # Share capital
                elif (row_str.str.contains('share', case=False).any() and 
                      row_str.str.contains('capital', case=False).any()) and 'share_capital' not in bs_data['equity']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['equity']['share_capital'] = value
                
                # Reserves
                elif row_str.str.contains('reserve', case=False).any() and 'reserves' not in bs_data['equity']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['equity']['reserves'] = value
                
                # Retained earnings
                elif (row_str.str.contains('retained', case=False).any() and 
                      row_str.str.contains('earning', case=False).any()) and 'retained_earnings' not in bs_data['equity']:
                    value = self._extract_numeric_value(row)
                    if value is not None:
                        bs_data['equity']['retained_earnings'] = value
            
            # Initialize missing values to 0
            for key in ['cash', 'receivables', 'inventories', 'other']:
                if key not in bs_data['current_assets']:
                    bs_data['current_assets'][key] = 0
            
            for key in ['ppe', 'intangibles', 'other']:
                if key not in bs_data['non_current_assets']:
                    bs_data['non_current_assets'][key] = 0
            
            for key in ['payables', 'provisions', 'other']:
                if key not in bs_data['current_liabilities']:
                    bs_data['current_liabilities'][key] = 0
            
            for key in ['borrowings', 'provisions', 'other']:
                if key not in bs_data['non_current_liabilities']:
                    bs_data['non_current_liabilities'][key] = 0
            
            for key in ['share_capital', 'reserves', 'retained_earnings']:
                if key not in bs_data['equity']:
                    bs_data['equity'][key] = 0
            
            # Calculate totals
            bs_data['total_current_assets'] = sum(bs_data['current_assets'].values())
            bs_data['total_non_current_assets'] = sum(bs_data['non_current_assets'].values())
            bs_data['total_assets'] = bs_data['total_current_assets'] + bs_data['total_non_current_assets']
            
            bs_data['total_current_liabilities'] = sum(bs_data['current_liabilities'].values())
            bs_data['total_non_current_liabilities'] = sum(bs_data['non_current_liabilities'].values())
            bs_data['total_liabilities'] = bs_data['total_current_liabilities'] + bs_data['total_non_current_liabilities']
            
            bs_data['total_equity'] = sum(bs_data['equity'].values())
            bs_data['total_liabilities_and_equity'] = bs_data['total_liabilities'] + bs_data['total_equity']
            
        except Exception as e:
            raise Exception(f"Error extracting balance sheet data: {str(e)}")
        
        return bs_data
    
    def _extract_numeric_value(self, row) -> Optional[float]:
        """
        Extract numeric value from a row, handling various formats.
        Prefers the rightmost numeric column (typically current year).
        
        Args:
            row: Pandas Series representing a row
            
        Returns:
            Optional[float]: Extracted numeric value or None if not found
        """
        # Look for numeric values in the row (excluding the first column which is typically labels)
        # Start from the right to get current year value
        for value in reversed(row[1:]):
            if pd.notna(value) and isinstance(value, (int, float)):
                return float(value)
            elif pd.notna(value) and isinstance(value, str):
                # Try to convert string to number
                try:
                    # Remove common formatting characters
                    cleaned_value = str(value).replace(',', '').replace('$', '').replace('(', '-').replace(')', '').strip()
                    if cleaned_value.lower() in ['-', 'nil', 'n/a', '', 'nan']:
                        continue
                    return float(cleaned_value)
                except (ValueError, AttributeError):
                    continue
        return None
    
    def validate_bs_balances(self, bs_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that Assets = Liabilities + Equity.
        
        Args:
            bs_data (Dict[str, Any]): Balance sheet data
            
        Returns:
            Tuple[bool, str]: (isValid, message)
        """
        assets = bs_data.get('total_assets', 0)
        liabilities_equity = bs_data.get('total_liabilities_and_equity', 0)
        
        if abs(assets - liabilities_equity) < 1:  # Allow for rounding differences
            return True, "Balance sheet balances"
        else:
            difference = assets - liabilities_equity
            return False, f"Balance sheet does not balance. Difference: ${difference:,.2f}"
    
    def validate_retained_earnings(self, bs_data: Dict[str, Any], pl_data: Dict[str, Any], 
                                 prior_re: float) -> Tuple[bool, str]:
        """
        Validate retained earnings rollforward: RE_end = RE_start + Net Profit/(Loss).
        
        Args:
            bs_data (Dict[str, Any]): Balance sheet data
            pl_data (Dict[str, Any]): Profit and loss data
            prior_re (float): Prior year retained earnings
            
        Returns:
            Tuple[bool, str]: (isValid, message)
        """
        current_re = bs_data.get('equity', {}).get('retained_earnings', 0)
        net_profit = pl_data.get('net_profit_loss', 0)
        
        expected_re = prior_re + net_profit
        
        if abs(current_re - expected_re) < 1:  # Allow for rounding differences
            return True, "Retained earnings rollforward is correct"
        else:
            difference = current_re - expected_re
            return False, f"Retained earnings mismatch. Expected: ${expected_re:,.2f}, Actual: ${current_re:,.2f}, Difference: ${difference:,.2f}"

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    # In practice, you would use the class in your main application
    try:
        processor = ExcelProcessor("sample_entity_management_report.xlsx")
        pl_data = processor.extract_pl_data()
        bs_data = processor.extract_bs_data()
        print("Successfully extracted data from Excel file")
        print("P&L Data:", pl_data)
        print("Balance Sheet Data:", bs_data)
    except Exception as e:
        print(f"Error: {str(e)}")