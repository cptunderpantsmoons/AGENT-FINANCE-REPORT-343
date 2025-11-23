# Quick Reference Guide

## Repository Structure

```
├── src/              # Source code
├── docs/             # Documentation  
├── data/samples/     # Sample files
├── scripts/          # Utility scripts
└── config/           # Configuration
```

## Quick Commands

### Run GUI
```bash
streamlit run src/gui_app.py
# or
./scripts/run_gui.sh
```

### Run CLI
```bash
python -m src.main --entity-name "Company" --current-year 2025 \
  --excel-file file.xlsx --prior-year-pdf file.pdf
```

### Test Application
```bash
python scripts/debug_fixes.py
```

## File Locations

- **Source Code**: `src/`
- **Documentation**: `docs/`
- **Sample Data**: `data/samples/`
- **Scripts**: `scripts/`
- **Config**: `config/`

## Important Files

- `README.md` - Main documentation
- `REPOSITORY_STRUCTURE.md` - Detailed structure
- `requirements.txt` - Dependencies
- `Procfile` - Railway deployment
- `SECRETS.md` - API keys (gitignored)

See [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) for complete details.

