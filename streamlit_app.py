#!/usr/bin/env python3
"""
Streamlit App for AASB Financial Statement Generator
Simple and robust version that avoids NameError issues.
"""

import sys
import os
import tempfile

# Add the src directory to the Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import from our package
try:
    from excel_processor import ExcelProcessor
    from pdf_parser import PDFParser
    from validator import FinancialStatementValidator
    from aasb_financial_statement_generator import AASBFinancialStatementGenerator
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    # Set page configuration
    st.set_page_config(
        page_title="AASB Financial Statement Generator",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize session state variables
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = None
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    if 'generated_file' not in st.session_state:
        st.session_state.generated_file = False
    
    # Main title
    st.title("📊 AASB Financial Statement Generator")
    st.write("Generate AASB-compliant financial statements for non-reporting entities")
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Home", "Upload Data", "Validation", "Preview", "Generate PDF"]
    )
    
    # Home Page
    if page == "Home":
        st.success("✅ App loaded successfully!")
        st.write("""
        ### 🚀 Quick Start
        1. **Upload Data** - Upload your Excel file and prior year PDF
        2. **Validate** - Check data quality and consistency  
        3. **Preview** - Review extracted financial data
        4. **Generate** - Create the final financial statements PDF
        
        ### 📁 Required Files
        - **Excel File**: Entity Management Reports (Consol PL and Consol BS sheets)
        - **PDF File**: Prior year Financial Statements PDF
        """)
        
        # Status indicators
        st.sidebar.subheader("Current Status")
        st.sidebar.write(f"Excel Data: {'✅' if st.session_state.excel_data else '❌'}")
        st.sidebar.write(f"PDF Data: {'✅' if st.session_state.pdf_data else '❌'}")
        st.sidebar.write(f"Validation: {'✅' if st.session_state.validation_results else '❌'}")
        st.sidebar.write(f"PDF Generated: {'✅' if st.session_state.generated_file else '❌'}")
    
    # Upload Data Page
    elif page == "Upload Data":
        st.subheader("📁 Upload Required Files")
        
        # Excel Upload
        st.write("### 📈 Excel File (Management Reports)")
        excel_file = st.file_uploader("Upload Excel file with Consol PL and Consol BS sheets", 
                                     type=['xlsx', 'xls'], key="excel")
        
        if excel_file is not None:
            try:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(excel_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process Excel
                processor = ExcelProcessor(tmp_path)
                pl_data = processor.extract_pl_data()
                bs_data = processor.extract_bs_data()
                
                # Store in session state
                st.session_state.excel_data = {
                    'pl_data': pl_data,
                    'bs_data': bs_data,
                    'file_name': excel_file.name
                }
                
                st.success(f"✅ Excel data loaded from {excel_file.name}")
                st.write("### Extracted P&L Data:")
                st.json(pl_data)
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # PDF Upload
        st.write("### 📄 Prior Year PDF")
        pdf_file = st.file_uploader("Upload prior year Financial Statements PDF", 
                                   type=['pdf'], key="pdf")
        
        if pdf_file is not None:
            try:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(pdf_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process PDF
                pdf_parser = PDFParser(tmp_path)
                pdf_data = {
                    'pl_data': pdf_parser.extract_income_statement_data(),
                    'bs_data': pdf_parser.extract_balance_sheet_data(),
                    'file_name': pdf_file.name
                }
                
                # Store in session state
                st.session_state.pdf_data = pdf_data
                
                st.success(f"✅ PDF data loaded from {pdf_file.name}")
                st.write("### Extracted PDF P&L Data:")
                st.json(pdf_data['pl_data'])
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Validation Page
    elif page == "Validation":
        st.subheader("✅ Data Validation")
        
        if not st.session_state.excel_data or not st.session_state.pdf_data:
            st.warning("⚠️ Please upload both Excel and PDF files first.")
        else:
            st.success("✅ Data loaded. Ready for validation.")
            
            # Entity info
            entity_name = st.text_input("Entity Name", value="Example Pty Ltd")
            current_year = st.number_input("Current Year", min_value=2020, max_value=2030, value=2025)
            
            if st.button("Run Validation"):
                try:
                    # Initialize validator
                    validator = FinancialStatementValidator(entity_name, current_year)
                    
                    # Run validation
                    is_valid, errors, warnings, queries = validator.validate_all(
                        bs_data=st.session_state.excel_data['bs_data'],
                        pl_data=st.session_state.excel_data['pl_data'],
                        prior_year_data=st.session_state.pdf_data['bs_data'],
                        prior_re=0,  # Simplified for testing
                        directors=[{'name': 'Test', 'title': 'Director'}],
                        compiler={'name': 'Test', 'title': 'CFO'},
                        tax_consolidation_entity="",
                        contingent_liability_text="",
                        notes_data={}
                    )
                    
                    # Store results
                    st.session_state.validation_results = {
                        'is_valid': is_valid,
                        'errors': errors,
                        'warnings': warnings
                    }
                    
                    # Show results
                    if errors:
                        st.error("❌ Errors found:")
                        for error in errors:
                            st.write(f"- {error}")
                    
                    if warnings:
                        st.warning("⚠️ Warnings:")
                        for warning in warnings:
                            st.write(f"- {warning}")
                    
                    if not errors and not warnings:
                        st.success("✅ All validations passed!")
                
                except Exception as e:
                    st.error(f"❌ Validation error: {str(e)}")
    
    # Preview Page
    elif page == "Preview":
        st.subheader("📊 Data Preview")
        
        if st.session_state.excel_data:
            st.write("### 📈 Excel P&L Data:")
            st.json(st.session_state.excel_data['pl_data'])
            st.write("### 📈 Excel Balance Sheet Data:")
            st.json(st.session_state.excel_data['bs_data'])
        else:
            st.warning("⚠️ No Excel data loaded")
        
        if st.session_state.pdf_data:
            st.write("### 📄 PDF P&L Data:")
            st.json(st.session_state.pdf_data['pl_data'])
        else:
            st.warning("⚠️ No PDF data loaded")
    
    # Generate PDF Page
    elif page == "Generate PDF":
        st.subheader("📤 Generate Financial Statements")
        
        if not st.session_state.excel_data or not st.session_state.validation_results:
            st.warning("⚠️ Please complete data upload and validation first.")
        else:
            st.success("✅ Ready to generate statements!")
            
            # Entity info
            entity_name = st.text_input("Entity Name", value="Example Pty Ltd")
            current_year = st.number_input("Current Year", min_value=2020, max_value=2030, value=2025)
            
            if st.button("Generate PDF"):
                try:
                    with st.spinner("Generating PDF..."):
                        # Create generator
                        generator = AASBFinancialStatementGenerator(
                            entity_name,
                            current_year,
                            st.session_state.pdf_data['bs_data']
                        )
                        
                        # Generate statements
                        filename = generator.generate_financial_statements(
                            st.session_state.excel_data['pl_data'],
                            st.session_state.excel_data['bs_data'],
                            {},
                            [{'name': 'Test Director', 'title': 'Director'}],
                            {'name': 'Test Compiler', 'title': 'CFO'}
                        )
                        
                        # Mark as generated
                        st.session_state.generated_file = True
                        
                        st.success(f"✅ PDF generated: {filename}")
                        
                        # Download button
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📥 Download PDF",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="application/pdf"
                            )
                
                except Exception as e:
                    st.error(f"❌ Generation error: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
    
except ImportError as e:
    st.error(f"❌ Import Error: {str(e)}")
    st.write("Please check dependencies and package structure.")
    
except Exception as e:
    st.error(f"❌ Unexpected Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
