# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

```bash
python main.py \
  --entity-name "Your Company Name" \
  --current-year 2025 \
  --excel-file path/to/your/excel/file.xlsx \
  --prior-year-pdf path/to/prior/year.pdf
```

## Required Files

1. **Prior Year PDF**: Financial statements from previous year (FY2024 for FY2025 statements)
2. **Excel File**: Current year management reports with sheets:
   - `Consol PL` (or similar) - Profit & Loss data
   - `Consol BS` (or similar) - Balance Sheet data

## What the System Does

1. ✅ Parses prior year PDF to extract structure and comparatives
2. ✅ Extracts current year data from Excel (source of truth)
3. ✅ Validates balance sheet balances
4. ✅ Validates retained earnings rollforward
5. ✅ Checks director/compiler information
6. ✅ Generates AASB-compliant PDF financial statements

## Output

Generates: `Financial Statements — [Entity Name] — For the Year Ended 30 June [Year].pdf`

## Troubleshooting

### "ModuleNotFoundError: No module named 'pdfplumber'"
**Solution**: Run `pip install -r requirements.txt`

### "Could not find 'Consol PL' sheet"
**Solution**: Rename your Excel sheet to match expected names, or the system will try common variations

### "Balance sheet does not balance"
**Solution**: Check your Excel file for calculation errors

### "Directors not found in PDF"
**Solution**: System will use default directors. You can manually verify after generation.

## Next Steps

1. Review generated PDF
2. Verify all figures match Excel source
3. Check note disclosures are complete
4. Confirm director/compiler information
5. Make any manual adjustments as needed

For detailed documentation, see `USAGE_GUIDE.md` and `IMPLEMENTATION_SUMMARY.md`.

