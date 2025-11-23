# Graphical User Interface Guide

## Overview

The GUI provides a user-friendly web interface for generating AASB-compliant financial statements with:
- **Drag-and-drop file uploads** for Excel and PDF files
- **Live preview** of financial data and statements
- **Editable fields** for directors, compiler, and notes
- **Validation checks** before generation
- **PDF preview and download**

## Getting Started

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the GUI:
```bash
streamlit run gui_app.py
```

Or use the provided script:
```bash
./run_gui.sh
```

3. Open your browser to `http://localhost:8501`

## Features

### 1. File Upload Section

**Drag-and-Drop Interface:**
- **Current Year Excel File** (Required)
  - Upload Excel file with `Consol PL` and `Consol BS` sheets
  - Automatically extracts financial data
  
- **Prior Year PDF** (Required)
  - Upload prior year financial statements PDF
  - Extracts structure, comparatives, notes, directors, compiler
  
- **Draft Current Year PDF** (Optional)
  - Upload draft PDF for structure hints only

### 2. Entity Information

Enter:
- **Entity Name**: Name of the entity
- **Financial Year**: Current financial year (e.g., 2025)

### 3. Financial Data Preview

Automatically displays:
- **Profit & Loss** items (Revenue, Expenses, Profit/Loss)
- **Balance Sheet** items (Assets, Liabilities, Equity)

### 4. Editable Fields

**Directors:**
- Add/remove directors
- Edit names and titles
- Defaults extracted from prior year PDF

**Compilation Signatory:**
- Edit compiler name and title
- Defaults extracted from prior year PDF

**Notes to Financial Statements:**
- Expandable sections for each note
- Edit note headings and content
- Notes extracted from prior year PDF

### 5. Validation

Click "Run Validation" to:
- Check balance sheet balances
- Validate retained earnings rollforward
- Verify director/compiler information
- Check note disclosures
- Run AI-powered validation (if enabled)

**Results Display:**
- ✅ Success messages for passed checks
- ⚠️ Warnings for items to review
- ❌ Errors that must be fixed

### 6. Preview & Generate

**Preview Statement:**
- Generates a preview PDF
- Displays in browser
- Download preview button available

**Generate Final PDF:**
- Generates final PDF after validation
- Download button for final PDF
- File named: `Financial Statements — [Entity Name] — For the Year Ended 30 June [Year].pdf`

## Workflow

1. **Upload Files**
   - Drag and drop Excel file (current year data)
   - Drag and drop Prior Year PDF (structure and comparatives)
   - (Optional) Upload Draft PDF

2. **Enter Entity Information**
   - Enter entity name
   - Set financial year

3. **Review Financial Data**
   - Check extracted P&L data
   - Check extracted Balance Sheet data
   - Verify figures are correct

4. **Edit Details**
   - Update director names/titles if needed
   - Update compiler information if needed
   - Edit note content as required

5. **Run Validation**
   - Click "Run Validation" button
   - Review validation results
   - Fix any errors before proceeding

6. **Preview Statement**
   - Click "Preview Statement" to see PDF
   - Review formatting and content
   - Make any final edits

7. **Generate Final PDF**
   - Click "Generate Final PDF"
   - Download the completed statement

## Sidebar Features

### Settings
- **Enable AI Validation**: Toggle AI-powered validation (requires OPENROUTER_API_KEY)

### Help
- Step-by-step instructions
- Quick reference guide

### About
- Compliance information
- AASB standards referenced

## Tips

1. **File Upload:**
   - Ensure Excel file has correct sheet names (`Consol PL`, `Consol BS`)
   - Prior Year PDF should be complete and readable
   - Files are processed automatically on upload

2. **Data Review:**
   - Always review extracted financial data
   - Compare with source Excel file
   - Check totals and calculations

3. **Editing:**
   - Directors can be added/removed using the number input
   - Notes can be edited individually
   - Changes are saved in session state

4. **Validation:**
   - Run validation before generating final PDF
   - Fix all errors before proceeding
   - Review warnings and queries

5. **Preview:**
   - Always preview before final generation
   - Check formatting and layout
   - Verify all sections are present

## Troubleshooting

### "Error processing Excel file"
- Check Excel file has correct sheet names
- Ensure file is not corrupted
- Verify data is in expected format

### "Error processing PDF file"
- Check PDF is not password protected
- Ensure PDF is readable
- Try a different PDF reader to verify

### "Validation errors"
- Review error messages
- Check balance sheet balances
- Verify retained earnings calculation
- Ensure all required fields are filled

### "PDF generation failed"
- Check all required files are uploaded
- Verify entity name is entered
- Ensure validation passed
- Check error messages for details

### Preview not displaying
- Check browser supports PDF viewing
- Try downloading and opening PDF
- Check browser console for errors

## Keyboard Shortcuts

- `Ctrl+R` or `F5`: Refresh page
- `Ctrl+Enter`: Submit form/run action
- `Esc`: Close modals/expanders

## Browser Compatibility

Recommended browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Session Management

- Data is stored in browser session
- Refresh page to reset session
- Files are processed in memory (not saved to disk)
- Generated PDFs can be downloaded

## Security

- Files are processed locally
- No data is sent to external servers (except AI validation if enabled)
- Generated PDFs are created locally
- Session data is browser-only

## Performance

- Large Excel files may take time to process
- Complex PDFs may require more processing time
- AI validation adds ~5-10 seconds per run
- Preview generation is fast (<5 seconds)

## Support

For issues:
1. Check error messages
2. Review validation results
3. Verify file formats
4. Check browser console for errors
5. Review documentation

## Future Enhancements

Potential additions:
- Save/load project files
- Multi-year comparison
- Custom templates
- Batch processing
- Export to Excel
- Print preview

