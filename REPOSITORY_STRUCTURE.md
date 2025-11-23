# Repository Structure

## Overview

The repository is now organized into a clean, professional structure following Python best practices.

## Directory Structure

```
AGENT-FINANCE-REPORT-343/
├── src/                          # Source code (Python modules)
│   ├── __init__.py              # Package initialization
│   ├── aasb_financial_statement_generator.py
│   ├── ai_service.py
│   ├── excel_processor.py
│   ├── gui_app.py               # Streamlit GUI application
│   ├── main.py                  # CLI application
│   ├── pdf_parser.py
│   └── validator.py
│
├── docs/                         # Documentation
│   ├── AI_FEATURES.md
│   ├── AI_INTEGRATION_SUMMARY.md
│   ├── DEBUGGING_COMPLETE.md
│   ├── DEBUG_REPORT.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── GITHUB_PUSH_INSTRUCTIONS.md
│   ├── GUI_GUIDE.md
│   ├── GUI_IMPLEMENTATION_SUMMARY.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── QUICK_RAILWAY_SETUP.md
│   ├── QUICK_START_GUI.md
│   ├── QUICK_START.md
│   ├── RAILWAY_CLI_INSTALL.md
│   ├── RAILWAY_DEPLOYMENT.md
│   ├── RAILWAY_SETUP_COMPLETE.md
│   ├── README_DEPLOYMENT.md
│   ├── SECURITY_SETUP.md
│   └── SOLUTION_SUMMARY.md
│
├── data/                         # Data files
│   └── samples/                  # Sample/test data
│       ├── sample2024 Financial Reportmaki .pdf
│       ├── sample2025DataMAKI.xlsx
│       ├── final2025maki14.pdf
│       └── Financial Statements — Example Pty Ltd — For the Year Ended 30 June 2025.pdf
│
├── scripts/                      # Utility scripts
│   ├── create_sample_excel.py
│   ├── debug_fixes.py
│   ├── install_railway_manual.sh
│   └── run_gui.sh
│
├── config/                       # Configuration files
│   └── .streamlit/
│       └── config.toml
│
├── .gitignore                    # Git ignore rules
├── Procfile                      # Railway deployment config
├── railway.json                  # Railway configuration
├── nixpacks.toml                 # Nixpacks build config
├── requirements.txt              # Python dependencies
├── runtime.txt                   # Python version
├── README.md                     # Main documentation
└── SECRETS.md                    # API keys (gitignored)
```

## File Organization

### Source Code (`src/`)
All Python modules are in the `src/` directory:
- Core modules: `excel_processor.py`, `pdf_parser.py`, `validator.py`
- Main applications: `main.py` (CLI), `gui_app.py` (Streamlit GUI)
- Generators: `aasb_financial_statement_generator.py`
- Services: `ai_service.py`

### Documentation (`docs/`)
All markdown documentation files:
- User guides
- Deployment guides
- Implementation summaries
- Quick start guides

### Data (`data/samples/`)
Sample files for testing:
- Sample Excel files
- Sample PDF files
- Generated output examples

### Scripts (`scripts/`)
Utility scripts:
- `run_gui.sh` - Launch GUI
- `debug_fixes.py` - Debugging tool
- `create_sample_excel.py` - Sample data generator
- `install_railway_manual.sh` - Railway CLI installer

### Configuration (`config/`)
Configuration files:
- Streamlit config
- Other app-specific configs

## Running the Application

### GUI Application
```bash
streamlit run src/gui_app.py
```

Or use the script:
```bash
./scripts/run_gui.sh
```

### CLI Application
```bash
python -m src.main --entity-name "Company" --current-year 2025 \
  --excel-file data.xlsx --prior-year-pdf prior.pdf
```

## Import Structure

All imports use relative imports within the `src/` package:
```python
from .excel_processor import ExcelProcessor
from .pdf_parser import PDFParser
from .validator import FinancialStatementValidator
```

## Deployment

Railway deployment files are in the root:
- `Procfile` - Updated to use `src/gui_app.py`
- `railway.json` - Updated paths
- `nixpacks.toml` - Updated paths

## Benefits

✅ **Clean organization** - Easy to find files
✅ **Professional structure** - Follows Python best practices
✅ **Scalable** - Easy to add new modules
✅ **Maintainable** - Clear separation of concerns
✅ **Deployment ready** - All paths updated

## Migration Notes

If you have existing code that imports from the old structure:
- Update imports to use `src.` prefix or add `src/` to `PYTHONPATH`
- Update file paths in scripts
- Update documentation references

