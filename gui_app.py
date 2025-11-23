"""
Streamlit GUI Application for AASB Financial Statement Generator
Features: Drag-and-drop uploads, preview, editing, and PDF download
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
import tempfile
import json
import copy
from typing import Dict, Any, Optional
import io

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from excel_processor import ExcelProcessor
from pdf_parser import PDFParser
from validator import FinancialStatementValidator
from aasb_financial_statement_generator import AASBFinancialStatementGenerator


# Page configuration
st.set_page_config(
    page_title="AASB Financial Statement Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Railway/Production configuration
if os.getenv('RAILWAY_ENVIRONMENT'):
    # Running on Railway
    st.markdown("""
    <style>
        .railway-badge {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: #0B0D0E;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 10px;
            z-index: 999;
        }
    </style>
    <div class="railway-badge">🚂 Railway</div>
    """, unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    .stFileUploader > div > div {
        border: 2px dashed #3498db;
        border-radius: 10px;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = None
    if 'prior_year_pdf' not in st.session_state:
        st.session_state.prior_year_pdf = None
    if 'draft_pdf' not in st.session_state:
        st.session_state.draft_pdf = None
    if 'pl_data' not in st.session_state:
        st.session_state.pl_data = None
    if 'bs_data' not in st.session_state:
        st.session_state.bs_data = None
    if 'prior_year_data' not in st.session_state:
        st.session_state.prior_year_data = None
    if 'notes_data' not in st.session_state:
        st.session_state.notes_data = {}
    if 'directors' not in st.session_state:
        st.session_state.directors = [
            {'name': 'Matthew Warnken', 'title': 'Director'},
            {'name': 'Gary Wyatt', 'title': 'Director'},
            {'name': 'Julian Turecek', 'title': 'Director'}
        ]
    if 'compiler' not in st.session_state:
        st.session_state.compiler = {
            'name': 'Allan Tuback',
            'title': 'Chief Financial Officer'
        }
    if 'entity_name' not in st.session_state:
        st.session_state.entity_name = ""
    if 'current_year' not in st.session_state:
        st.session_state.current_year = 2025
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    if 'generated_pdf_path' not in st.session_state:
        st.session_state.generated_pdf_path = None


def process_excel_file(uploaded_file) -> Optional[Dict[str, Any]]:
    """Process uploaded Excel file."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        processor = ExcelProcessor(tmp_path)
        pl_data = processor.extract_pl_data()
        bs_data = processor.extract_bs_data()
        
        os.unlink(tmp_path)  # Clean up
        
        return {'pl': pl_data, 'bs': bs_data}
    except Exception as e:
        st.error(f"Error processing Excel file: {str(e)}")
        return None


def process_pdf_file(uploaded_file, file_type: str) -> Optional[Dict[str, Any]]:
    """Process uploaded PDF file."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        parser = PDFParser(tmp_path)
        
        if file_type == 'prior_year':
            entity_name = parser.extract_entity_name()
            prior_year = parser.extract_prior_year()
            pl_data = parser.extract_income_statement_data()
            bs_data = parser.extract_balance_sheet_data()
            notes = parser.extract_notes_structure()
            directors = parser.extract_directors_info()
            compiler = parser.extract_compiler_info()
            
            # Convert notes to dict format
            notes_dict = {}
            for note in notes:
                notes_dict[f"note_{note['number']}"] = note
            
            result = {
                'entity_name': entity_name,
                'prior_year': prior_year,
                'pl_data': pl_data,
                'bs_data': bs_data,
                'notes': notes_dict,
                'directors': directors or st.session_state.directors,
                'compiler': compiler or st.session_state.compiler
            }
        else:  # draft
            result = {'parser': parser, 'path': tmp_path}
        
        return result
    except Exception as e:
        st.error(f"Error processing PDF file: {str(e)}")
        return None


def render_file_upload_section():
    """Render file upload section with drag-and-drop."""
    st.markdown('<div class="section-header">📁 Upload Files</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Current Year Excel File")
        st.markdown("*Required: Entity Management Reports*")
        excel_file = st.file_uploader(
            "Upload Excel file",
            type=['xlsx', 'xls'],
            key='excel_upload',
            help="Upload the Excel file containing current year financial data (Consol PL and Consol BS sheets)"
        )
        
        if excel_file is not None:
            if st.session_state.excel_data is None or st.session_state.excel_data.get('filename') != excel_file.name:
                with st.spinner("Processing Excel file..."):
                    data = process_excel_file(excel_file)
                    if data:
                        st.session_state.excel_data = {
                            'filename': excel_file.name,
                            'pl_data': data['pl'],
                            'bs_data': data['bs']
                        }
                        st.session_state.pl_data = data['pl']
                        st.session_state.bs_data = data['bs']
                        st.success(f"✓ Excel file processed: {excel_file.name}")
    
    with col2:
        st.markdown("### Prior Year PDF")
        st.markdown("*Required: Prior year financial statements*")
        prior_pdf = st.file_uploader(
            "Upload Prior Year PDF",
            type=['pdf'],
            key='prior_pdf_upload',
            help="Upload the prior year financial statements PDF for structure and comparatives"
        )
        
        if prior_pdf is not None:
            if st.session_state.prior_year_pdf is None or st.session_state.prior_year_pdf.get('filename') != prior_pdf.name:
                with st.spinner("Processing Prior Year PDF..."):
                    data = process_pdf_file(prior_pdf, 'prior_year')
                    if data:
                        st.session_state.prior_year_pdf = {
                            'filename': prior_pdf.name,
                            'data': data
                        }
                        st.session_state.prior_year_data = {**data['pl_data'], **data['bs_data']}
                        st.session_state.notes_data = data.get('notes', {})
                        if data.get('entity_name'):
                            st.session_state.entity_name = data['entity_name']
                        if data.get('directors'):
                            st.session_state.directors = data['directors']
                        if data.get('compiler'):
                            st.session_state.compiler = data['compiler']
                        st.success(f"✓ Prior Year PDF processed: {prior_pdf.name}")
    
    with col3:
        st.markdown("### Draft Current Year PDF")
        st.markdown("*Optional: For structure hints*")
        draft_pdf = st.file_uploader(
            "Upload Draft PDF",
            type=['pdf'],
            key='draft_pdf_upload',
            help="Optional: Upload draft current year PDF for structure hints only"
        )
        
        if draft_pdf is not None:
            st.session_state.draft_pdf = {
                'filename': draft_pdf.name,
                'file': draft_pdf
            }
            st.info(f"📄 Draft PDF uploaded: {draft_pdf.name}")


def render_entity_info_section():
    """Render entity information input section."""
    st.markdown('<div class="section-header">🏢 Entity Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        entity_name = st.text_input(
            "Entity Name",
            value=st.session_state.entity_name,
            key='entity_name_input',
            help="Name of the entity for the financial statements"
        )
        st.session_state.entity_name = entity_name
    
    with col2:
        current_year = st.number_input(
            "Financial Year",
            min_value=2000,
            max_value=2100,
            value=st.session_state.current_year,
            key='current_year_input',
            help="Current financial year (e.g., 2025)"
        )
        st.session_state.current_year = int(current_year)


def render_financial_data_preview():
    """Render preview of extracted financial data."""
    st.markdown('<div class="section-header">📊 Financial Data Preview</div>', unsafe_allow_html=True)
    
    if st.session_state.pl_data and st.session_state.bs_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Profit & Loss")
            pl_df = pd.DataFrame([
                ["Revenue", f"${st.session_state.pl_data.get('revenue', 0):,.0f}"],
                ["Cost of Sales", f"${st.session_state.pl_data.get('cost_of_sales', 0):,.0f}"],
                ["Gross Profit", f"${st.session_state.pl_data.get('gross_profit', 0):,.0f}"],
                ["Other Income", f"${st.session_state.pl_data.get('other_income', 0):,.0f}"],
                ["Distribution Costs", f"${st.session_state.pl_data.get('distribution_costs', 0):,.0f}"],
                ["Admin Expenses", f"${st.session_state.pl_data.get('administrative_expenses', 0):,.0f}"],
                ["Profit Before Tax", f"${st.session_state.pl_data.get('profit_before_tax', 0):,.0f}"],
                ["Income Tax", f"${st.session_state.pl_data.get('income_tax_expense', 0):,.0f}"],
                ["Net Profit/(Loss)", f"${st.session_state.pl_data.get('net_profit_loss', 0):,.0f}"]
            ], columns=["Item", "Amount"])
            st.dataframe(pl_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### Balance Sheet")
            bs_df = pd.DataFrame([
                ["Total Assets", f"${st.session_state.bs_data.get('total_assets', 0):,.0f}"],
                ["Total Liabilities", f"${st.session_state.bs_data.get('total_liabilities', 0):,.0f}"],
                ["Total Equity", f"${st.session_state.bs_data.get('total_equity', 0):,.0f}"],
                ["Cash", f"${st.session_state.bs_data.get('current_assets', {}).get('cash', 0):,.0f}"],
                ["Receivables", f"${st.session_state.bs_data.get('current_assets', {}).get('receivables', 0):,.0f}"],
                ["PPE", f"${st.session_state.bs_data.get('non_current_assets', {}).get('ppe', 0):,.0f}"],
                ["Share Capital", f"${st.session_state.bs_data.get('equity', {}).get('share_capital', 0):,.0f}"],
                ["Retained Earnings", f"${st.session_state.bs_data.get('equity', {}).get('retained_earnings', 0):,.0f}"]
            ], columns=["Item", "Amount"])
            st.dataframe(bs_df, use_container_width=True, hide_index=True)
    else:
        st.info("Upload Excel file to see financial data preview")


def render_editable_fields():
    """Render editable fields for directors, compiler, and notes."""
    st.markdown('<div class="section-header">✏️ Edit Statement Details</div>', unsafe_allow_html=True)
    
    # Directors
    st.markdown("### Directors")
    num_directors = st.number_input("Number of Directors", min_value=1, max_value=10, value=len(st.session_state.directors), key='num_directors')
    
    # Ensure directors list has correct length
    while len(st.session_state.directors) < num_directors:
        st.session_state.directors.append({'name': '', 'title': 'Director'})
    while len(st.session_state.directors) > num_directors:
        st.session_state.directors.pop()
    
    for i, director in enumerate(st.session_state.directors):
        col1, col2 = st.columns([3, 1])
        with col1:
            director['name'] = st.text_input(f"Director {i+1} Name", value=director.get('name', ''), key=f'director_name_{i}')
        with col2:
            director['title'] = st.text_input(f"Title", value=director.get('title', 'Director'), key=f'director_title_{i}')
    
    # Compiler
    st.markdown("### Compilation Signatory")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.compiler['name'] = st.text_input("Compiler Name", value=st.session_state.compiler.get('name', ''), key='compiler_name')
    with col2:
        st.session_state.compiler['title'] = st.text_input("Title", value=st.session_state.compiler.get('title', ''), key='compiler_title')
    
    # Notes editing
    st.markdown("### Notes to Financial Statements")
    if st.session_state.notes_data:
        note_numbers = sorted([int(k.split('_')[1]) for k in st.session_state.notes_data.keys() if k.startswith('note_')])
        
        for note_num in note_numbers:
            note_key = f"note_{note_num}"
            if note_key in st.session_state.notes_data:
                note = st.session_state.notes_data[note_key]
                with st.expander(f"Note {note_num}: {note.get('heading', 'Untitled')}"):
                    note['heading'] = st.text_input(f"Heading", value=note.get('heading', ''), key=f'note_heading_{note_num}')
                    note['content'] = st.text_area(f"Content", value=note.get('content', ''), height=150, key=f'note_content_{note_num}')
    else:
        st.info("Notes will be extracted from prior year PDF or use defaults")


def render_validation_section():
    """Render validation section."""
    st.markdown('<div class="section-header">✅ Validation</div>', unsafe_allow_html=True)
    
    if st.button("Run Validation", type="primary", use_container_width=True):
        if not st.session_state.pl_data or not st.session_state.bs_data:
            st.error("Please upload Excel file first")
            return
        
        if not st.session_state.prior_year_pdf:
            st.error("Please upload Prior Year PDF first")
            return
        
        with st.spinner("Running validation checks..."):
            try:
                validator = FinancialStatementValidator(
                    st.session_state.entity_name,
                    st.session_state.current_year,
                    use_ai=os.getenv('OPENROUTER_API_KEY') is not None
                )
                
                prior_re = st.session_state.prior_year_data.get('equity', {}).get('retained_earnings', 0)
                if prior_re == 0:
                    prior_re = st.session_state.prior_year_data.get('retained_earnings', 0)
                
                # Create a copy of BS data with updated retained earnings for validation
                bs_data_for_validation = copy.deepcopy(st.session_state.bs_data)
                bs_data_for_validation['equity']['retained_earnings'] = prior_re + st.session_state.pl_data.get('net_profit_loss', 0)
                bs_data_for_validation['total_equity'] = sum(bs_data_for_validation['equity'].values())
                bs_data_for_validation['total_liabilities_and_equity'] = bs_data_for_validation['total_liabilities'] + bs_data_for_validation['total_equity']
                # Recalculate assets totals
                bs_data_for_validation['total_current_assets'] = sum(bs_data_for_validation['current_assets'].values())
                bs_data_for_validation['total_non_current_assets'] = sum(bs_data_for_validation['non_current_assets'].values())
                bs_data_for_validation['total_assets'] = bs_data_for_validation['total_current_assets'] + bs_data_for_validation['total_non_current_assets']
                
                is_valid, errors, warnings, queries = validator.validate_all(
                    bs_data=bs_data_for_validation,
                    pl_data=st.session_state.pl_data,
                    prior_year_data=st.session_state.prior_year_data,
                    prior_re=prior_re,
                    directors=st.session_state.directors,
                    compiler=st.session_state.compiler,
                    tax_consolidation_entity=None,
                    contingent_liability_text=None,
                    notes_data=st.session_state.notes_data
                )
                
                st.session_state.validation_results = {
                    'is_valid': is_valid,
                    'errors': errors,
                    'warnings': warnings,
                    'queries': queries
                }
                
                # Display results
                if errors:
                    for error in errors:
                        st.markdown(f'<div class="error-box">{error}</div>', unsafe_allow_html=True)
                
                if queries:
                    for query in queries:
                        st.markdown(f'<div class="warning-box">{query}</div>', unsafe_allow_html=True)
                
                if warnings:
                    for warning in warnings:
                        st.warning(warning)
                
                if is_valid and not errors:
                    st.success("✓ All validation checks passed!")
                
            except Exception as e:
                st.error(f"Validation error: {str(e)}")


def render_preview_and_generate():
    """Render preview and PDF generation section."""
    st.markdown('<div class="section-header">📄 Preview & Generate PDF</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Preview Statement", use_container_width=True):
            if not st.session_state.pl_data or not st.session_state.bs_data:
                st.error("Please upload Excel file first")
                return
            
            if not st.session_state.entity_name:
                st.error("Please enter entity name")
                return
            
            # Generate preview HTML
            try:
                with st.spinner("Generating preview..."):
                    # Calculate retained earnings
                    prior_re = st.session_state.prior_year_data.get('equity', {}).get('retained_earnings', 0)
                    if prior_re == 0:
                        prior_re = st.session_state.prior_year_data.get('retained_earnings', 0)
                    
                    # Update retained earnings - deep copy to avoid modifying original
                    bs_data_copy = copy.deepcopy(st.session_state.bs_data)
                    
                    # Update retained earnings
                    bs_data_copy['equity']['retained_earnings'] = prior_re + st.session_state.pl_data.get('net_profit_loss', 0)
                    
                    # Recalculate all totals to ensure balance
                    bs_data_copy['total_equity'] = sum(bs_data_copy['equity'].values())
                    bs_data_copy['total_liabilities_and_equity'] = bs_data_copy['total_liabilities'] + bs_data_copy['total_equity']
                    
                    # Recalculate total_assets from components to ensure accuracy
                    bs_data_copy['total_current_assets'] = sum(bs_data_copy['current_assets'].values())
                    bs_data_copy['total_non_current_assets'] = sum(bs_data_copy['non_current_assets'].values())
                    bs_data_copy['total_assets'] = bs_data_copy['total_current_assets'] + bs_data_copy['total_non_current_assets']
                    
                    # Validate balance - if it doesn't balance, it's a data issue
                    if abs(bs_data_copy['total_assets'] - bs_data_copy['total_liabilities_and_equity']) > 1:
                        difference = bs_data_copy['total_assets'] - bs_data_copy['total_liabilities_and_equity']
                        st.warning(f"⚠️ Balance sheet imbalance: ${difference:,.2f}. Please check Excel data.")
                    
                    # Generate preview
                    generator = AASBFinancialStatementGenerator(
                        st.session_state.entity_name,
                        st.session_state.current_year,
                        st.session_state.prior_year_data,
                        notes_structure=st.session_state.notes_data
                    )
                    
                    # Create temporary PDF for preview
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_path = tmp_file.name
                    
                    # Generate PDF
                    generator.generate_financial_statements(
                        st.session_state.pl_data,
                        bs_data_copy,
                        st.session_state.notes_data,
                        st.session_state.directors,
                        st.session_state.compiler
                    )
                    
                    # Move to temp location
                    expected_filename = f"Financial Statements — {st.session_state.entity_name} — For the Year Ended 30 June {st.session_state.current_year}.pdf"
                    if os.path.exists(expected_filename):
                        import shutil
                        shutil.move(expected_filename, tmp_path)
                        st.session_state.generated_pdf_path = tmp_path
                        
                        # Display PDF
                        with open(tmp_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                            st.download_button(
                                label="📥 Download Preview PDF",
                                data=pdf_bytes,
                                file_name=expected_filename,
                                mime="application/pdf"
                            )
                        
                        # Show PDF using base64 encoding
                        import base64
                        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    else:
                        st.error("PDF generation failed")
            except Exception as e:
                st.error(f"Preview generation error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    with col2:
        if st.button("Generate Final PDF", type="primary", use_container_width=True):
            if not st.session_state.pl_data or not st.session_state.bs_data:
                st.error("Please upload Excel file first")
                return
            
            if not st.session_state.entity_name:
                st.error("Please enter entity name")
                return
            
            # Check validation
            if st.session_state.validation_results and not st.session_state.validation_results['is_valid']:
                st.error("Please fix validation errors before generating PDF")
                return
            
            try:
                with st.spinner("Generating final PDF..."):
                    # Calculate retained earnings
                    prior_re = st.session_state.prior_year_data.get('equity', {}).get('retained_earnings', 0)
                    if prior_re == 0:
                        prior_re = st.session_state.prior_year_data.get('retained_earnings', 0)
                    
                    # Update retained earnings - deep copy to avoid modifying original
                    bs_data_copy = copy.deepcopy(st.session_state.bs_data)
                    
                    # Update retained earnings
                    bs_data_copy['equity']['retained_earnings'] = prior_re + st.session_state.pl_data.get('net_profit_loss', 0)
                    
                    # Recalculate all totals to ensure balance
                    bs_data_copy['total_equity'] = sum(bs_data_copy['equity'].values())
                    bs_data_copy['total_liabilities_and_equity'] = bs_data_copy['total_liabilities'] + bs_data_copy['total_equity']
                    
                    # Recalculate total_assets from components to ensure accuracy
                    bs_data_copy['total_current_assets'] = sum(bs_data_copy['current_assets'].values())
                    bs_data_copy['total_non_current_assets'] = sum(bs_data_copy['non_current_assets'].values())
                    bs_data_copy['total_assets'] = bs_data_copy['total_current_assets'] + bs_data_copy['total_non_current_assets']
                    
                    # Validate balance - if it doesn't balance, it's a data issue
                    if abs(bs_data_copy['total_assets'] - bs_data_copy['total_liabilities_and_equity']) > 1:
                        difference = bs_data_copy['total_assets'] - bs_data_copy['total_liabilities_and_equity']
                        st.warning(f"⚠️ Balance sheet imbalance: ${difference:,.2f}. Please check Excel data.")
                    
                    # Generate PDF
                    generator = AASBFinancialStatementGenerator(
                        st.session_state.entity_name,
                        st.session_state.current_year,
                        st.session_state.prior_year_data,
                        notes_structure=st.session_state.notes_data
                    )
                    
                    filename = generator.generate_financial_statements(
                        st.session_state.pl_data,
                        bs_data_copy,
                        st.session_state.notes_data,
                        st.session_state.directors,
                        st.session_state.compiler
                    )
                    
                    st.session_state.generated_pdf_path = filename
                    
                    # Provide download
                    if os.path.exists(filename):
                        with open(filename, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                            st.download_button(
                                label="📥 Download Final PDF",
                                data=pdf_bytes,
                                file_name=os.path.basename(filename),
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        # Show PDF preview
                        import base64
                        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                        
                        st.success(f"✓ PDF generated successfully: {os.path.basename(filename)}")
                    else:
                        st.error(f"PDF file not found: {filename}")
                    
            except Exception as e:
                st.error(f"PDF generation error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


def main():
    """Main application."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📊 AASB Financial Statement Generator</div>', unsafe_allow_html=True)
    st.markdown("**Generate AASB-compliant financial statements for Australian non-reporting entities**")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        use_ai = st.checkbox(
            "Enable AI Validation",
            value=os.getenv('OPENROUTER_API_KEY') is not None,
            help="Requires OPENROUTER_API_KEY environment variable"
        )
        
        if use_ai and not os.getenv('OPENROUTER_API_KEY'):
            st.warning("⚠️ OPENROUTER_API_KEY not set. AI features disabled.")
        
        # Show deployment info
        if os.getenv('RAILWAY_ENVIRONMENT'):
            st.markdown("---")
            st.markdown("### 🚂 Deployment")
            st.info("Running on Railway")
            if os.getenv('RAILWAY_PUBLIC_DOMAIN'):
                st.code(os.getenv('RAILWAY_PUBLIC_DOMAIN'))
        
        st.markdown("---")
        st.markdown("### 📚 Help")
        st.markdown("""
        1. **Upload Files**: Drag and drop Excel and PDF files
        2. **Enter Entity Info**: Fill in entity name and year
        3. **Review Data**: Check extracted financial data
        4. **Edit Details**: Modify directors, compiler, notes
        5. **Validate**: Run validation checks
        6. **Preview**: Preview the statement
        7. **Generate**: Download final PDF
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This tool generates AASB-compliant financial statements for Australian non-reporting entities.
        
        **Compliance:**
        - AASB 101
        - AASB 108
        - AASB 1048
        """)
    
    # Main content
    render_file_upload_section()
    
    if st.session_state.excel_data and st.session_state.prior_year_pdf:
        render_entity_info_section()
        render_financial_data_preview()
        render_editable_fields()
        render_validation_section()
        render_preview_and_generate()
    else:
        st.info("👆 Please upload the required files (Excel and Prior Year PDF) to begin")


if __name__ == "__main__":
    main()

