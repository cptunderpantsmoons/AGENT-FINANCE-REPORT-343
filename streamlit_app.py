#!/usr/bin/env python3
"""
Streamlit App for AASB Financial Statement Generator
Complete full-featured application with all functionality.
"""

import sys
import os
import tempfile
from datetime import datetime

# Add the src directory to the Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import from our package
try:
    from excel_processor import ExcelProcessor
    from pdf_parser import PDFParser
    from validator import FinancialStatementValidator
    from aasb_financial_statement_generator import AASBFinancialStatementGenerator
    from ai_service import AIService
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    # Set page configuration
    st.set_page_config(
        page_title="AASB Financial Statement Generator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state properly
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = None
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    if 'generated_file' not in st.session_state:
        st.session_state.generated_file = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    
    # Sidebar for navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "📁 Upload Data", "✅ Validation", "📊 Preview", "📤 Generate PDF"]
    )
    
    # Helper function to check if data is available
    def check_data_status():
        excel_loaded = st.session_state.excel_data is not None
        pdf_loaded = st.session_state.pdf_data is not None
        validation_done = st.session_state.validation_results is not None
        pdf_generated = st.session_state.generated_file
        
        return excel_loaded, pdf_loaded, validation_done, pdf_generated
    
    # Get current status
    excel_loaded, pdf_loaded, validation_done, pdf_generated = check_data_status()
    
    # Home Page
    if page == "🏠 Home":
        st.title("📊 AASB Financial Statement Generator")
        st.write("Generate AASB-compliant financial statements for non-reporting entities")
        
        st.markdown("""
        ### 🚀 Quick Start
        1. **Upload Data** - Upload your Excel file and prior year PDF
        2. **Validate** - Check data quality and consistency  
        3. **Preview** - Review extracted financial data
        4. **Generate** - Create the final financial statements PDF
        
        ### 📁 Required Files
        - **Excel File**: Entity Management Reports (Consol PL and Consol BS sheets)
        - **PDF File**: Prior year Financial Statements PDF
        
        ### ✨ Features
        - 📊 Excel data extraction and validation
        - 📄 PDF parsing and data extraction
        - 🤖 AI-powered validation and enhancement
        - 📋 AASB-compliant statement generation
        - 🔍 Comprehensive data validation
        """)
        
        # Display current status
        st.sidebar.subheader("📊 Current Status")
        if excel_loaded:
            st.sidebar.success("✅ Excel data loaded")
        else:
            st.sidebar.warning("⚠️ Excel data needed")
            
        if pdf_loaded:
            st.sidebar.success("✅ PDF data loaded") 
        else:
            st.sidebar.warning("⚠️ PDF data needed")
        
        # Progress indicator
        st.subheader("Progress Tracker")
        steps = [
            ("📁 Upload Data", excel_loaded and pdf_loaded),
            ("✅ Validation", validation_done),
            ("📤 Generate PDF", pdf_generated)
        ]
        
        for step_name, completed in steps:
            if completed:
                st.write(f"✅ {step_name}")
            else:
                st.write(f"⏳ {step_name}")
    
    # Upload Data Page
    elif page == "📁 Upload Data":
        st.title("📁 Upload Required Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Excel File (Management Reports)")
            excel_file = st.file_uploader(
                "Upload Excel file with Consol PL and Consol BS sheets",
                type=['xlsx', 'xls'],
                key="excel_upload_v2"
            )
            
            if excel_file is not None:
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                        tmp_file.write(excel_file.getvalue())
                        tmp_excel_path = tmp_file.name
                    
                    # Process Excel data
                    processor = ExcelProcessor(tmp_excel_path)
                    
                    # Extract data
                    pl_data = processor.extract_pl_data()
                    bs_data = processor.extract_bs_data()
                    
                    # Store in session state
                    st.session_state.excel_data = {
                        'processor': processor,
                        'pl_data': pl_data,
                        'bs_data': bs_data,
                        'file_name': excel_file.name
                    }
                    
                    st.success(f"✅ Excel data extracted from {excel_file.name}")
                    
                    # Show extracted data preview
                    st.write("### Extracted P&L Data:")
                    st.json(pl_data)
                    
                    st.write("### Extracted Balance Sheet Data:")
                    st.json(bs_data)
                    
                    # Clean up temp file
                    os.unlink(tmp_excel_path)
                    
                except Exception as e:
                    st.error(f"❌ Error processing Excel file: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        with col2:
            st.subheader("📄 Prior Year PDF")
            pdf_file = st.file_uploader(
                "Upload prior year Financial Statements PDF",
                type=['pdf'],
                key="pdf_upload_v2"
            )
            
            if pdf_file is not None:
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(pdf_file.getvalue())
                        tmp_pdf_path = tmp_file.name
                    
                    # Process PDF data
                    pdf_parser = PDFParser(tmp_pdf_path)
                    
                    # Extract data
                    pl_pdf_data = pdf_parser.extract_income_statement_data()
                    bs_pdf_data = pdf_parser.extract_balance_sheet_data()
                    notes_data = pdf_parser.extract_notes_structure()
                    
                    # Store in session state
                    st.session_state.pdf_data = {
                        'parser': pdf_parser,
                        'pl_data': pl_pdf_data,
                        'bs_data': bs_pdf_data,
                        'notes_data': notes_data,
                        'file_name': pdf_file.name
                    }
                    
                    st.success(f"✅ PDF data extracted from {pdf_file.name}")
                    
                    # Show extracted data preview
                    st.write("### Extracted PDF P&L Data:")
                    st.json(pl_pdf_data)
                    
                    st.write("### Extracted PDF Balance Sheet Data:")
                    st.json(bs_pdf_data)
                    
                    # Clean up temp file
                    os.unlink(tmp_pdf_path)
                    
                except Exception as e:
                    st.error(f"❌ Error processing PDF file: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Validation Page
    elif page == "✅ Validation":
        st.title("✅ Data Validation")
        
        if not excel_loaded or not pdf_loaded:
            st.warning("⚠️ Please upload both Excel and PDF files first.")
        else:
            st.success("✅ Both data sources are loaded. Running validation...")
            
            try:
                # Get entity information
                entity_name = st.text_input("Entity Name", value="Example Pty Ltd")
                current_year = st.number_input("Current Financial Year", min_value=2020, max_value=2030, value=2025)
                
                # Initialize validator
                validator = FinancialStatementValidator(entity_name, current_year)
                
                # Get prior year retained earnings
                prior_re = st.session_state.pdf_data['bs_data'].get('equity', {}).get('retained_earnings', 0)
                if prior_re == 0:
                    prior_re = st.session_state.pdf_data['bs_data'].get('retained_earnings', 0)
                
                # Run validation
                is_valid, errors, warnings, queries = validator.validate_all(
                    bs_data=st.session_state.excel_data['bs_data'],
                    pl_data=st.session_state.excel_data['pl_data'],
                    prior_year_data=st.session_state.pdf_data['bs_data'],
                    prior_re=prior_re,
                    directors=[{'name': 'Test Director', 'title': 'Director'}],
                    compiler={'name': 'Test Compiler', 'title': 'CFO'},
                    tax_consolidation_entity="",
                    contingent_liability_text="",
                    notes_data={}
                )
                
                # Store validation results
                st.session_state.validation_results = {
                    'is_valid': is_valid,
                    'errors': errors,
                    'warnings': warnings,
                    'queries': queries
                }
                
                # Display results
                if errors:
                    st.error("❌ Validation Errors Found:")
                    for error in errors:
                        st.write(f"- {error}")
                
                if warnings:
                    st.warning("⚠️ Validation Warnings:")
                    for warning in warnings:
                        st.write(f"- {warning}")
                
                if not errors and not warnings:
                    st.success("✅ All validations passed!")
                
                # Show data quality analysis
                if 'processor' in st.session_state.excel_data:
                    analysis = st.session_state.excel_data['processor'].analyze_data_quality()
                    st.write("### Data Quality Analysis:")
                    st.json(analysis)
                
            except Exception as e:
                st.error(f"❌ Validation error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    # Preview Page
    elif page == "📊 Preview":
        st.title("📊 Data Preview")
        
        if st.session_state.excel_data:
            st.subheader("📈 Excel Data")
            st.write("### Profit & Loss Data:")
            st.json(st.session_state.excel_data['pl_data'])
            
            st.write("### Balance Sheet Data:")
            st.json(st.session_state.excel_data['bs_data'])
        else:
            st.warning("⚠️ No Excel data loaded")
        
        if st.session_state.pdf_data:
            st.subheader("📄 PDF Data")
            st.write("### PDF P&L Data:")
            st.json(st.session_state.pdf_data['pl_data'])
            
            st.write("### PDF Balance Sheet Data:")
            st.json(st.session_state.pdf_data['bs_data'])
        else:
            st.warning("⚠️ No PDF data loaded")
        
        # Comparison view
        if st.session_state.excel_data and st.session_state.pdf_data:
            st.subheader("🔍 Data Comparison")
            excel_bs = st.session_state.excel_data['bs_data']
            pdf_bs = st.session_state.pdf_data['bs_data']
            
            comparison_data = {
                'Excel Total Assets': excel_bs.get('total_assets', 0),
                'PDF Total Assets': pdf_bs.get('total_assets', 0),
                'Excel Total Equity': excel_bs.get('total_equity', 0),
                'PDF Total Equity': pdf_bs.get('total_equity', 0),
                'Excel Net Profit': st.session_state.excel_data['pl_data'].get('net_profit_loss', 0),
                'PDF Net Profit': st.session_state.pdf_data['pl_data'].get('net_profit_loss', 0)
            }
            
            st.write("### Key Figures Comparison:")
            st.json(comparison_data)
    
    # Generate PDF Page
    elif page == "📤 Generate PDF":
        st.title("📤 Generate Financial Statements")
        
        if not excel_loaded or not validation_done:
            st.warning("⚠️ Please complete data upload and validation first.")
        else:
            st.success("✅ Ready to generate financial statements!")
            
            # Get additional inputs
            entity_name = st.text_input("Entity Name", value="Example Pty Ltd")
            current_year = st.number_input("Current Financial Year", min_value=2020, max_value=2030, value=2025)
            
            # Optional AI enhancement
            use_ai = st.checkbox("Enable AI-powered enhancements (requires API key)", value=False)
            
            if st.button("🚀 Generate Financial Statements"):
                try:
                    with st.spinner("Generating financial statements..."):
                        # Get prior year data
                        prior_year_data = st.session_state.pdf_data['bs_data']
                        prior_year = current_year - 1
                        
                        # Create generator
                        generator = AASBFinancialStatementGenerator(
                            entity_name,
                            current_year,
                            prior_year_data
                        )
                        
                        # Generate statements
                        filename = generator.generate_financial_statements(
                            st.session_state.excel_data['pl_data'],
                            st.session_state.excel_data['bs_data'],
                            {},
                            [{'name': 'Test Director', 'title': 'Director'}],
                            {'name': 'Test Compiler', 'title': 'CFO'}
                        )
                        
                        # Store generated file status
                        st.session_state.generated_file = True
                        
                        st.success(f"✅ Financial statements generated: {filename}")
                        
                        # Offer download
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📥 Download PDF",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="application/pdf"
                            )
                        
                        # Show generated file info
                        st.write("### Generated File Details:")
                        st.write(f"- **File**: {filename}")
                        st.write(f"- **Size**: {os.path.getsize(filename) if os.path.exists(filename) else 'Unknown'} bytes")
                        st.write(f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        st.write(f"- **Entity**: {entity_name}")
                        st.write(f"- **Year**: {current_year}")
                
                except Exception as e:
                    st.error(f"❌ Error generating statements: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Sidebar status - using safe boolean checks
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Session Status")
    st.sidebar.write(f"Excel Data: {'✅' if excel_loaded else '❌'}")
    st.sidebar.write(f"PDF Data: {'✅' if pdf_loaded else '❌'}")
    st.sidebar.write(f"Validation: {'✅' if validation_done else '❌'}")
    st.sidebar.write(f"PDF Generated: {'✅' if pdf_generated else '❌'}")
    
    # Additional sidebar info
    if excel_loaded:
        st.sidebar.write(f"Excel File: {st.session_state.excel_data['file_name']}")
    if pdf_loaded:
        st.sidebar.write(f"PDF File: {st.session_state.pdf_data['file_name']}")
    
except ImportError as e:
    st.error(f"❌ Import Error: {str(e)}")
    st.write("There was an issue importing the required modules.")
    st.write("Please check that all dependencies are installed and the package structure is correct.")
    
except Exception as e:
    st.error(f"❌ Unexpected Error: {str(e)}")
    st.write("An unexpected error occurred. Please check the application logs.")
    import traceback
    st.code(traceback.format_exc())
