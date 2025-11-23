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

## Requirements

- Python 3.7+
- Dependencies listed in [requirements.txt](requirements.txt)
- (Optional) OpenRouter API key for AI features - set `OPENROUTER_API_KEY` environment variable

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface (Recommended)

Launch the web-based GUI with drag-and-drop file uploads:

```bash
streamlit run gui_app.py
```

Or use the provided script:
```bash
./run_gui.sh
```

Then open your browser to `http://localhost:8501`

**GUI Features:**
- Drag-and-drop file uploads
- Live preview of financial data
- Editable fields for directors, compiler, and notes
- Validation checks before generation
- PDF preview and download

See [GUI_GUIDE.md](GUI_GUIDE.md) for detailed instructions.

### Command Line Interface

The generator can be used from the command line:

```bash
python main.py \
  --entity-name "Example Pty Ltd" \
  --current-year 2025 \
  --excel-file data.xlsx \
  --prior-year-pdf prior.pdf
```

### Programmatic Usage

The generator can be used programmatically by importing the `AASBFinancialStatementGenerator` class:

```python
from aasb_financial_statement_generator import AASBFinancialStatementGenerator

# Initialize the generator
generator = AASBFinancialStatementGenerator("Company Name", 2025)

# Define your financial data
pl_data = {
    'revenue': 1000000,
    # ... other P&L items
}

bs_data = {
    'current_assets': {
        'cash': 150000,
        # ... other current assets
    },
    # ... other balance sheet items
}

# Generate the financial statements
filename = generator.generate_financial_statements(
    pl_data, 
    bs_data, 
    notes_data, 
    directors, 
    compiler
)
```

## Compliance

This generator ensures compliance with:
- AASB 101 Presentation of Financial Statements
- AASB 108 Accounting Policies, Changes in Accounting Estimates and Errors
- AASB 1048 Interpretation of Standards

The generated statements are suitable for non-reporting entities as defined under Australian accounting standards.

## AI Features

The system includes optional AI-powered features for enhanced accuracy:

- **Enhanced PDF Parsing**: Better extraction from complex PDF layouts
- **AI Validation**: Deep analysis of balance sheet relationships and note disclosures
- **Cross-Validation**: Ensures Excel and PDF data consistency
- **Compliance Checking**: Validates AASB requirements automatically

See [AI_FEATURES.md](AI_FEATURES.md) for detailed documentation.

To enable AI features:
```bash
export OPENROUTER_API_KEY="your-api-key"
```

To disable AI features:
```bash
python main.py ... --no-ai
```

## Customization

To customize for your specific entity:
1. Modify the data structures to match your financial data
2. Update director and compiler information
3. Adjust note disclosures as required for your specific circumstances

## Validation Checks

The generator includes built-in validation for:
- Balance sheet balancing (Assets = Liabilities + Equity)
- Retained earnings roll-forward calculations
- Director information consistency
- Required note disclosures

Any discrepancies will be flagged before final generation.