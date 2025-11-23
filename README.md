# AASB Financial Statement Generator

A comprehensive application for generating AASB-compliant financial statements for non-reporting entities.

## Streamlit Deployment

### Method 1: Using the Streamlit App Entry Point (Recommended)

1. **Deploy the `streamlit_app.py` file**
   - This file contains the proper path configuration to resolve import issues
   - It adds the `src` directory to the Python path before importing modules

2. **Required Files for Deployment:**
   - `streamlit_app.py` - Main Streamlit application
   - `requirements.txt` - Python dependencies
   - `src/` directory - Source code (keep this structure intact)

### Method 2: Using setup.py

1. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

2. **Deploy with your Streamlit app:**
   ```python
   from aasb_financial_statement_generator import AASBFinancialStatementGenerator
   # Your app code here
   ```

## Troubleshooting Import Issues

### If you encounter the original error:
```
ModuleNotFoundError: No module named 'excel_processor'
```

**Solution:** Make sure you're using the `streamlit_app.py` entry point, which properly configures the Python path.

### Alternative Solutions:

1. **Set PYTHONPATH environment variable:**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/src"
   ```

2. **Use relative imports in your Streamlit app:**
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
   
   from excel_processor import ExcelProcessor
   ```

## Dependencies

All required dependencies are listed in `requirements.txt`. Key dependencies include:

- `pandas` - Data processing
- `numpy` - Numerical operations
- `openpyxl` - Excel file processing
- `pdfplumber` - PDF text extraction
- `reportlab` - PDF generation
- `streamlit` - Web application framework

## Project Structure

```
AGENT FINANCE REPORT 343/
├── streamlit_app.py          # Main Streamlit entry point (use this for deployment)
├── requirements.txt          # Python dependencies
├── setup.py                 # Package configuration
├── src/                     # Source code directory
│   ├── __init__.py
│   ├── excel_processor.py
│   ├── pdf_parser.py
│   ├── validator.py
│   ├── aasb_financial_statement_generator.py
│   ├── ai_service.py
│   └── main.py
└── .streamlit/              # Streamlit configuration
    └── config.toml
```

## Quick Start

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run locally for testing:**
   ```bash
   streamlit run streamlit_app.py
   ```
4. **Deploy to Streamlit Cloud using `streamlit_app.py`**

## Notes

- The `streamlit_app.py` file is specifically designed to resolve the import path issues
- Keep the `src/` directory structure intact during deployment
- Make sure all dependencies in `requirements.txt` are available in the deployment environment
