# Quick Start - GUI Application

## Launch the GUI

### Option 1: Using the script
```bash
./run_gui.sh
```

### Option 2: Direct command
```bash
streamlit run gui_app.py
```

### Option 3: With custom port
```bash
streamlit run gui_app.py --server.port 8501
```

## First Steps

1. **Open Browser**: Navigate to `http://localhost:8501`

2. **Upload Files**:
   - Drag and drop your **Excel file** (current year data)
   - Drag and drop **Prior Year PDF** (for structure and comparatives)

3. **Enter Information**:
   - Entity name
   - Financial year (e.g., 2025)

4. **Review & Edit**:
   - Check extracted financial data
   - Edit directors, compiler, notes as needed

5. **Validate**:
   - Click "Run Validation"
   - Fix any errors

6. **Generate**:
   - Click "Preview Statement" to review
   - Click "Generate Final PDF" to download

## Features at a Glance

✅ **Drag-and-drop** file uploads  
✅ **Live preview** of financial data  
✅ **Editable** directors, compiler, notes  
✅ **Validation** before generation  
✅ **PDF preview** in browser  
✅ **Download** final PDF  

## Troubleshooting

**GUI won't start?**
```bash
pip install streamlit
streamlit run gui_app.py
```

**Files not uploading?**
- Check file formats (Excel: .xlsx, PDF: .pdf)
- Ensure files are not corrupted
- Try smaller files first

**Preview not showing?**
- Try downloading the PDF instead
- Check browser console for errors
- Use Chrome or Firefox

For detailed help, see [GUI_GUIDE.md](GUI_GUIDE.md)

