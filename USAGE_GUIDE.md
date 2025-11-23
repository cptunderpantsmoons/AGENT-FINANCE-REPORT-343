# AASB-Compliant Financial Statement Generator - Usage Guide

## Overview

This system generates AASB-compliant financial statements for Australian private companies preparing special-purpose financial statements under AASB standards for non-reporting entities, as permitted by AASB 101, AASB 108, and AASB 1048.

## Installation

```bash
pip install -r requirements.txt
```

## Required Inputs

### 1. Prior Year Financial Reports PDF
- **File**: `[PriorYear]_Financial_Reports.pdf`
- **Purpose**: Authoritative reference for:
  - Structure, numbering, note headings, and phrasing
  - Accounting policy wording (Notes 1–3 especially)
  - Prior-year comparative figures (e.g., FY2024 numbers used in FY2025 statements)
  - Formatting, layout, and director declaration template

### 2. Current Year Entity Management Reports Excel
- **File**: `[CurrentYear]_Entity_Management_Reports_[Date]_vX.xlsx`
- **Purpose**: Primary source of truth for current-year actuals
- **Tabs to prioritize**:
  - `Consol PL`: Income Statement & EBITDA
  - `Consol BS`: Balance Sheet & Equity rollforwards
  - `Consol CFS`: Optional validation only (do not source data here unless PL/BS conflict)

### 3. Draft Current Year Financial Statements PDF (Optional)
- **File**: `[DraftCurrentYear]_Financial_Statements.pdf`
- **Purpose**: Used only for:
  - Sectioning hints (e.g., if prior-year PDF is missing a note used in draft)
  - Detecting new disclosures (e.g., new contingent liabilities, new intangibles)
- **Important**: Never trust numerical values — always override with Excel data

## Usage

### Basic Command

```bash
python main.py \
  --entity-name "Example Pty Ltd" \
  --current-year 2025 \
  --excel-file sample2025DataMAKI.xlsx \
  --prior-year-pdf sample2024.pdf
```

### With Draft PDF (Optional)

```bash
python main.py \
  --entity-name "Example Pty Ltd" \
  --current-year 2025 \
  --excel-file sample2025DataMAKI.xlsx \
  --prior-year-pdf sample2024.pdf \
  --draft-current-pdf draft2025.pdf
```

## Validation Checks

The system performs comprehensive validation before generating the final PDF:

### Mandatory Checks (STOP if fail):

1. **Balance Sheet Balances**
   - Verifies: Total Assets = Total Liabilities + Total Equity
   - ❌ **STOP** if mismatch detected

2. **Retained Earnings Rollforward**
   - Verifies: RE_end = RE_start + Net Profit/(Loss)
   - ❌ **STOP** if mismatch detected

3. **Tax Consolidation Disclosure**
   - Checks Note 3(b)(i) references correct head entity
   - ❌ **STOP** if head entity name differs from prior year & unconfirmed

4. **Contingent Liability Consistency**
   - If prior year had TENBS/other commitment, FY2025 must retain identical wording
   - ❌ **QUERY** if missing or altered without confirmation

5. **Director Names & Titles**
   - Must match prior-year declaration
   - ❌ **CONFIRM** before updating sign date

6. **Compilation Signatory**
   - Must be qualified (e.g., Allan Tuback, CFO)
   - ❌ **VERIFY** credentials if changed

### Additional Validations (warn but proceed):

- Cash accounts: Confirm closure of legacy accounts
- Related party loan split: Ensure Excel shows correct CL/NCL split
- Deferred tax: Note 4 must explain why no income tax benefit recognised

## Output

The system generates a PDF titled:
```
Financial Statements — [Entity Name] — For the Year Ended 30 June [CurrentYear]
```

### Output Sections (in order):

1. Title Page
2. Contents
3. Income Statement (Statement of Profit or Loss and Other Comprehensive Income)
4. Appropriation Statement (if applicable)
5. Balance Sheet (Statement of Financial Position)
6. Notes 1–14 (retains all prior headings; adds new only if substantiated & approved)
7. Directors' Declaration (same signatories)
8. Compilation Report (CFO-signed)

### Formatting:

- All amounts in AUD, rounded to nearest dollar (no decimals)
- Print-ready A4 PDF (portrait)
- Footer: "Page X" (page numbers)
- Sign Date: Leave blank or use 30 June [CurrentYear] — do not auto-fill actual signing date

## Key Principles

1. **Consistency over novelty**: If uncertain, match prior-year phrasing exactly
2. **Excel is source of truth**: All FY2025 figures must be extracted only from Excel
3. **Prior year for comparatives**: Use final audited prior-year values (from PDF), not draft or Excel prior-year estimates
4. **Zero-balance notes**: All note headings from prior year must appear — even if $0 balances

## Troubleshooting

### Balance Sheet Doesn't Balance

**Error**: "Balance sheet does not balance. Difference: $X"

**Solution**: 
1. Check Excel file for data entry errors
2. Verify all line items are correctly extracted
3. Ensure totals are calculated correctly in Excel

### Retained Earnings Mismatch

**Error**: "Retained earnings mismatch. Expected: $X, Actual: $Y"

**Solution**:
1. Verify prior year retained earnings from PDF
2. Check current year net profit/loss from Excel
3. Ensure calculation: RE_end = RE_start + Net Profit/(Loss)

### Missing Sheet Error

**Error**: "Could not find 'Consol PL' sheet in Excel file"

**Solution**:
1. Check Excel file has sheets named exactly:
   - `Consol PL` (or `ConsolPL`, `PL`, `Profit Loss`, `Income Statement`)
   - `Consol BS` (or `ConsolBS`, `BS`, `Balance Sheet`, `Statement of Financial Position`)
2. Rename sheets if necessary to match expected names

### PDF Parsing Issues

**Warning**: "Directors not found in PDF, using defaults"

**Solution**:
1. Ensure prior year PDF is readable and not corrupted
2. Check PDF contains Directors' Declaration section
3. System will use default directors if not found

## File Structure

```
├── main.py                              # Main application entry point
├── aasb_financial_statement_generator.py # PDF generation engine
├── excel_processor.py                   # Excel data extraction
├── pdf_parser.py                        # Prior year PDF parsing
├── validator.py                         # Comprehensive validation
├── requirements.txt                     # Python dependencies
├── README.md                            # General documentation
├── USAGE_GUIDE.md                       # This file
└── [Generated PDFs]                     # Output files
```

## Compliance

This system ensures compliance with:
- AASB 101 (Presentation of Financial Statements)
- AASB 108 (Accounting Policies, Changes in Estimates & Errors)
- AASB 1048 (Interpretation of Standards)
- Section 295 of the Corporations Act 2001

## Support

For issues or questions:
1. Check validation error messages for specific guidance
2. Review Excel file structure matches expected format
3. Verify prior year PDF is complete and readable
4. Ensure all required inputs are provided

## Example Workflow

1. **Prepare Inputs**:
   - Ensure prior year PDF is available
   - Prepare Excel file with current year data
   - (Optional) Prepare draft current year PDF

2. **Run Generator**:
   ```bash
   python main.py --entity-name "Your Company" --current-year 2025 \
     --excel-file your_data.xlsx --prior-year-pdf prior_year.pdf
   ```

3. **Review Validation**:
   - Check all validation checks pass
   - Address any queries or warnings
   - Confirm director/compiler information

4. **Generate PDF**:
   - System generates final PDF
   - Review output for accuracy
   - Make manual adjustments if needed

5. **Final Review**:
   - Cross-check key figures
   - Verify note disclosures
   - Confirm formatting matches prior year

