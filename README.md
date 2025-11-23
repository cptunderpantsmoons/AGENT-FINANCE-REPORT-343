# AASB-Compliant Financial Statement Generator

This tool generates AASB-compliant financial statements for Australian non-reporting entities in accordance with AASB 101, AASB 108, and AASB 1048.

## Features

- **Web-Based GUI**: User-friendly interface with drag-and-drop file uploads, live preview, and editing capabilities
- **AI-Powered Validation** (Optional): Uses OpenRouter API with multiple models for:
  - Enhanced PDF parsing and data extraction
  - Balance sheet relationship validation with reasoning
  - Note disclosure compliance checking
  - Cross-validation between Excel and PDF sources
  - Tax consolidation disclosure validation
- Generates PDF financial statements compliant with Australian Accounting Standards for non-reporting entities
- Maintains consistent formatting with prior year statements
- Includes all required sections:
  - Statement of Profit or Loss and Other Comprehensive Income
  - Statement of Financial Position (Balance Sheet)
  - Notes to the Financial Statements
  - Directors' Declaration
  - Independent Compilation Report
- Automatically formats currency values in AUD, rounded to nearest dollar
- Includes comparative figures from prior year
- Validates key financial relationships (Assets = Liabilities + Equity)

## Repository Structure

```
├── src/              # Source code (Python modules)
├── docs/             # Documentation
├── data/samples/     # Sample data files
├── scripts/          # Utility scripts
├── config/           # Configuration files
└── README.md         # This file
```

See [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) for detailed structure.

## Requirements

- Python 3.7+
- Dependencies listed in [requirements.txt](requirements.txt)
- (Optional) OpenRouter API key for AI features - set `OPENROUTER_API_KEY` environment variable

## Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface (Recommended)

Launch the web-based GUI with drag-and-drop file uploads:

```bash
streamlit run src/gui_app.py
```

Or use the provided script:
```bash
./scripts/run_gui.sh
```

Then open your browser to `http://localhost:8501`

**GUI Features:**
- Drag-and-drop file uploads
- Live preview of financial data
- Editable fields for directors, compiler, and notes
- Validation checks before generation
- PDF preview and download

See [docs/GUI_GUIDE.md](docs/GUI_GUIDE.md) for detailed instructions.

### Command Line Interface

The generator can be used from the command line:

```bash
python -m src.main \
  --entity-name "Example Pty Ltd" \
  --current-year 2025 \
  --excel-file data.xlsx \
  --prior-year-pdf prior.pdf
```

### Programmatic Usage

The generator can be used programmatically:

```python
import sys
sys.path.insert(0, 'src')

from aasb_financial_statement_generator import AASBFinancialStatementGenerator
from excel_processor import ExcelProcessor

# Initialize the generator
generator = AASBFinancialStatementGenerator("Company Name", 2025)

# Process Excel data
processor = ExcelProcessor("data.xlsx")
pl_data = processor.extract_pl_data()
bs_data = processor.extract_bs_data()

# Generate the financial statements
filename = generator.generate_financial_statements(
    pl_data, 
    bs_data, 
    notes_data, 
    directors, 
    compiler
)
```

## AI Features

The system includes optional AI-powered features for enhanced accuracy:

- **Enhanced PDF Parsing**: Better extraction from complex PDF layouts
- **AI Validation**: Deep analysis of balance sheet relationships and note disclosures
- **Cross-Validation**: Ensures Excel and PDF data consistency
- **Compliance Checking**: Validates AASB requirements automatically

See [docs/AI_FEATURES.md](docs/AI_FEATURES.md) for detailed documentation.

To enable AI features:
```bash
export OPENROUTER_API_KEY="your-api-key"
```

To disable AI features:
```bash
python -m src.main ... --no-ai
```

## Compliance

This generator ensures compliance with:
- AASB 101 Presentation of Financial Statements
- AASB 108 Accounting Policies, Changes in Accounting Estimates and Errors
- AASB 1048 Interpretation of Standards

The generated statements are suitable for non-reporting entities as defined under Australian accounting standards.

## Validation Checks

The generator includes built-in validation for:
- Balance sheet balancing (Assets = Liabilities + Equity)
- Retained earnings roll-forward calculations
- Director information consistency
- Required note disclosures
- AI-powered validation (if enabled)

Any discrepancies will be flagged before final generation.

## Documentation

- [Repository Structure](REPOSITORY_STRUCTURE.md) - Project organization
- [GUI Guide](docs/GUI_GUIDE.md) - Complete GUI documentation
- [Usage Guide](docs/USAGE_GUIDE.md) - Detailed usage instructions
- [AI Features](docs/AI_FEATURES.md) - AI-powered features guide
- [Railway Deployment](docs/RAILWAY_DEPLOYMENT.md) - Deployment guide

## Customization

To customize for your specific entity:
1. Modify the data structures to match your financial data
2. Update director and compiler information
3. Adjust note disclosures as required for your specific circumstances

## License

This project is for internal use. All rights reserved.

# AgentStatementsfinalee
