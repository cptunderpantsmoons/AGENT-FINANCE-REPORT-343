# AASB-Compliant Financial Statement Generator for Non-Reporting Entities

## Overview

This solution provides a complete system for generating AASB-compliant financial statements for Australian private companies classified as non-reporting entities under AASB standards. The system automates the creation of special-purpose financial statements in accordance with AASB 101, AASB 108, and AASB 1048.

## Key Features

### 1. Automated PDF Generation
- Creates print-ready A4 PDF documents
- Maintains identical structure and wording to prior-year statements
- Includes all required sections:
  - Statement of Profit or Loss and Other Comprehensive Income
  - Statement of Financial Position (Balance Sheet)
  - Notes to the Financial Statements
  - Directors' Declaration
  - Independent Compilation Report

### 2. AASB Compliance
- Complies with Australian Accounting Standards for non-reporting entities
- Retains only disclosures required by AASB 101, 108, and 1048
- Formats all amounts in AUD, rounded to nearest dollar
- Uses final audited prior-year values for comparatives

### 3. Data Processing
- Reads financial data from Excel management reports
- Extracts data from specifically named sheets:
  - "Consol PL" for Profit and Loss
  - "Consol BS" for Balance Sheet
- Validates key financial relationships:
  - Assets = Liabilities + Equity
  - Retained Earnings rollforward calculations

### 4. Validation & Error Handling
- Performs mandatory validation checks before final generation:
  - Balance Sheet Balancing
  - Retained Earnings Rollforward
  - Director Information Consistency
  - Required Note Disclosures
- Halts generation with clear error messages if validations fail

## File Structure

```
├── aasb_financial_statement_generator.py  # Main PDF generation engine
├── excel_processor.py                     # Excel data extraction and validation
├── main.py                               # Command-line interface
├── requirements.txt                      # Python dependencies
├── README.md                             # User documentation
├── SOLUTION_SUMMARY.md                   # This file
├── sample_entity_management_report.xlsx  # Sample Excel data
├── sample_prior_year.pdf                 # Sample prior year PDF
├── create_sample_excel.py                # Utility to create sample Excel files
└── "Financial Statements — Example Pty Ltd — For the Year Ended 30 June 2025.pdf"  # Generated output
```

## Usage

### Installation
```bash
pip install -r requirements.txt
```

### Command Line Usage
```bash
python3 main.py \
  --entity-name "Entity Name" \
  --current-year 2025 \
  --excel-file path/to/entity_management_report.xlsx \
  --prior-year-pdf path/to/prior_year_financial_reports.pdf
```

### Programmatic Usage
```python
from aasb_financial_statement_generator import AASBFinancialStatementGenerator
from excel_processor import ExcelProcessor

# Process Excel data
processor = ExcelProcessor("path/to/entity_management_report.xlsx")
pl_data = processor.extract_pl_data()
bs_data = processor.extract_bs_data()

# Generate financial statements
generator = AASBFinancialStatementGenerator("Entity Name", 2025, prior_year_data)
filename = generator.generate_financial_statements(
    pl_data, 
    bs_data, 
    notes_data, 
    directors, 
    compiler
)
```

## Validation Checks

The system performs the following mandatory validations:

1. **Balance Sheet Balancing**
   - Verifies Total Assets = Total Liabilities + Total Equity
   - Stops generation if mismatch detected

2. **Retained Earnings Rollforward**
   - Validates RE_end = RE_start + Net Profit/(Loss)
   - Stops generation if mismatch detected

3. **Director Information Consistency**
   - Ensures director names and titles match prior year
   - Confirms compilation signatory credentials

4. **Required Note Disclosures**
   - Maintains all note headings from prior year (even $0 balances)
   - Adds new disclosures only when substantiated

## Compliance Assurance

- Follows AASB standards for non-reporting entities
- Maintains continuity with prior-year phrasing and structure
- Preserves director intent over exhaustive disclosure
- Complies with section 295 of the Corporations Act 2001

## Customization

The system can be customized for specific entities by:
- Modifying data extraction logic in excel_processor.py
- Updating director and compiler information
- Adjusting note disclosures based on entity-specific requirements
- Adding new validation checks as needed

## Dependencies

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- reportlab >= 3.6.0
- openpyxl >= 3.0.7
- xlsxwriter >= 1.4.0

## Error Handling

The system implements a robust error handling protocol:
- Validates all inputs before processing
- Performs intermediate validation during data extraction
- Conducts final validation before PDF generation
- Provides clear error messages for troubleshooting
- Halts generation immediately when critical errors are detected

## Future Enhancements

Potential improvements for future versions:
- PDF parsing for prior-year data extraction
- Enhanced Excel template matching
- Additional AASB standard compliance checks
- Web-based user interface
- Integration with accounting software APIs