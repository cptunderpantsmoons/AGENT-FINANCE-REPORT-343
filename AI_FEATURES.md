# AI-Powered Features

## Overview

The system includes AI-powered features using OpenRouter API to ensure perfect results. AI is used for:
- Enhanced PDF parsing and data extraction
- Balance sheet relationship validation
- Note disclosure validation and generation
- Cross-validation between Excel and PDF sources
- Tax consolidation disclosure validation

## Setup

### 1. Get OpenRouter API Key

1. Sign up at https://openrouter.ai/
2. Get your API key from the dashboard
3. Set it as an environment variable:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Or add to your `.env` file:
```
OPENROUTER_API_KEY=your-api-key-here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Available AI Models

The system uses different models for different tasks:

1. **x-ai/grok-4.1-fast** (Primary)
   - Best for reasoning and complex validation tasks
   - 2M context window
   - Reasoning mode enabled for complex analysis
   - Used for: Balance sheet validation, note validation

2. **google/gemini-2.5-flash-lite** (Fast tasks)
   - Fast, cost-effective
   - Used for: Cross-validation, tax consolidation checks

3. **openai/gpt-4.1-nano** (General purpose)
   - General purpose tasks
   - Used for: Note content generation

4. **openai/gpt-5-mini** (Fallback)
   - Used if reasoning fails or primary model unavailable

5. **nvidia/nemotron-nano-12b-v2-vl** (Document intelligence)
   - Specialized for document understanding, OCR, charts
   - Used for: Enhanced PDF text extraction

## AI Features

### 1. Enhanced PDF Parsing

**What it does:**
- Extracts structured data from complex PDF layouts
- Identifies financial figures that standard parsing might miss
- Extracts director and compiler information more accurately
- Improves note structure extraction

**When it runs:**
- Automatically during PDF parsing if AI is enabled
- Falls back to standard parsing if AI fails

**Example:**
```python
# AI extracts additional data from PDF text
ai_financial = ai_service.extract_data_from_pdf_text(pdf_text, "financial")
```

### 2. Balance Sheet Validation

**What it does:**
- Validates Assets = Liabilities + Equity using AI reasoning
- Checks retained earnings rollforward
- Identifies unusual relationships or potential errors
- Validates totals are correctly calculated

**When it runs:**
- During validation step if AI is enabled
- Provides detailed analysis and recommendations

**Example output:**
```
✓ AI balance sheet validation passed
⚠️ AI Recommendation: Consider reviewing related party loan classification
```

### 3. Note Disclosure Validation

**What it does:**
- Validates all required AASB disclosures are present
- Identifies missing or inadequate disclosures
- Recommends improvements to note content
- Ensures compliance with AASB 101, 108, 1048

**When it runs:**
- During validation step if AI is enabled and notes are available

**Example output:**
```
⚠️ AI NOTE VALIDATION: Missing disclosures detected
   - Note 4: Property, plant and equipment - needs depreciation policy
   - Note 7: Related party transactions - disclosure required
```

### 4. Cross-Validation

**What it does:**
- Compares Excel data (source of truth) with PDF data
- Identifies discrepancies between sources
- Validates calculations
- Ensures consistency

**When it runs:**
- During validation step if AI is enabled

**Example output:**
```
✓ AI cross-validation passed
⚠️ AI Cross-Validation: Prior year revenue differs by $5,000 (likely rounding)
```

### 5. Tax Consolidation Validation

**What it does:**
- Validates tax consolidation disclosure references correct head entity
- Checks disclosure follows AASB requirements
- Ensures wording consistency

**When it runs:**
- During validation step if tax consolidation entity is identified

### 6. Note Content Generation

**What it does:**
- Generates AASB-compliant note content based on financial data
- Ensures appropriate level of detail for non-reporting entities
- Uses Australian accounting terminology

**When it runs:**
- Can be called manually for missing notes
- Currently available as utility function

## Usage

### Enable AI (Default)

```bash
python main.py \
  --entity-name "Example Pty Ltd" \
  --current-year 2025 \
  --excel-file data.xlsx \
  --prior-year-pdf prior.pdf
```

AI is enabled by default if `OPENROUTER_API_KEY` is set.

### Disable AI

```bash
python main.py \
  --entity-name "Example Pty Ltd" \
  --current-year 2025 \
  --excel-file data.xlsx \
  --prior-year-pdf prior.pdf \
  --no-ai
```

### Programmatic Usage

```python
from ai_service import AIService

# Initialize AI service
ai_service = AIService()  # Uses OPENROUTER_API_KEY env var

# Validate balance sheet
is_valid, message, analysis = ai_service.validate_balance_sheet_relationships(
    bs_data, pl_data
)

# Validate notes
is_complete, missing, analysis = ai_service.validate_note_disclosures(
    notes_data, bs_data, pl_data
)

# Extract data from PDF
pdf_text = "..."
financial_data = ai_service.extract_data_from_pdf_text(pdf_text, "financial")
```

## Cost Considerations

AI features use OpenRouter API which charges per token. Approximate costs:

- **Grok 4.1 Fast**: ~$0.01-0.02 per validation
- **Gemini Flash**: ~$0.001-0.002 per validation
- **GPT Nano**: ~$0.001-0.002 per generation
- **Nemotron VL**: ~$0.002-0.005 per extraction

**Total per run**: Approximately $0.05-0.10 for full AI validation

## Error Handling

The system gracefully handles AI failures:

1. **API Key Missing**: Falls back to standard validation
2. **API Error**: Logs warning, continues with standard methods
3. **Model Unavailable**: Falls back to alternative model
4. **Timeout**: Logs warning, continues without AI

All AI features are optional - the system works without AI, but AI enhances accuracy.

## Best Practices

1. **Always set API key**: Even if you disable AI, having it available is useful
2. **Review AI recommendations**: AI provides suggestions, but human review is essential
3. **Monitor costs**: Check OpenRouter dashboard for usage
4. **Test without AI first**: Ensure basic functionality works, then enable AI
5. **Use AI for complex cases**: Especially useful for complex PDF layouts or unusual disclosures

## Troubleshooting

### "OpenRouter API key required"
**Solution**: Set `OPENROUTER_API_KEY` environment variable

### "AI validation failed"
**Solution**: 
- Check internet connection
- Verify API key is valid
- Check OpenRouter service status
- System will continue without AI

### "Model unavailable"
**Solution**: System automatically falls back to alternative models

### High costs
**Solution**: 
- Use `--no-ai` flag to disable AI
- AI is optional - system works without it
- Consider using only for complex cases

## Future Enhancements

Potential AI enhancements:
- Automated note content generation for all notes
- Intelligent figure reconciliation
- Automated disclosure checklist generation
- Multi-year trend analysis
- Anomaly detection in financial data

