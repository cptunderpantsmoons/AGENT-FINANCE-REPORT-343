#!/usr/bin/env python3
"""
Ultra-simple Streamlit App - No NameError Version
This version eliminates all potential NameError issues by using simple, direct code.
"""

import sys
import os
import tempfile

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Import required modules
    import streamlit as st
    import pandas as pd
    import numpy as np
    from excel_processor import ExcelProcessor
    from pdf_parser import PDFParser
    from validator import FinancialStatementValidator
    from aasb_financial_statement_generator import AASBFinancialStatementGenerator
    
    # Set page configuration
    st.set_page_config(
        page_title="AASB Financial Statement Generator",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize session state with simple boolean flags
    if 'has_excel' not in st.session_state:
        st.session_state.has_excel = False
    if 'has_pdf' not in st.session_state:
        st.session_state.has_pdf = False
    if 'has_validation' not in st.session_state:
        st.session_state.has_validation = False
    if 'has_generated' not in st.session_state:
        st.session_state.has_generated = False
    
    # Main title and description
    st.title("📊 AASB Financial Statement Generator")
    st.write("Generate AASB-compliant financial statements for non-reporting entities")
    
    # Simple navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page:",
        ["Home", "Upload Excel", "Upload PDF", "Validate", "Generate"]
    )
    
    # Status indicators - using simple boolean checks
    st.sidebar.subheader("Status")
    excel_status = "✅" if st.session_state.has_excel else "❌"
    pdf_status = "✅" if st.session_state.has_pdf else "❌"
    validation_status = "✅" if st.session_state.has_validation else "❌"
    generation_status = "✅" if st.session_state.has_generated else "❌"
    
    st.sidebar.write(f"Excel Loaded: {excel_status}")
    st.sidebar.write(f"PDF Loaded: {pdf_status}")
    st.sidebar.write(f"Validation Done: {validation_status}")
    st.sidebar.write(f"PDF Generated: {generation_status}")
    
    # Home page
    if page == "Home":
        st.subheader("Welcome!")
        st.write("This app helps you generate AASB-compliant financial statements.")
        st.write("Use the navigation to upload files and generate statements.")
        
        # Show current status
        st.write("### Current Status:")
        st.write(f"- Excel Data: {'Loaded' if st.session_state.has_excel else 'Not Loaded'}")
        st.write(f"- PDF Data: {'Loaded' if st.session_state.has_pdf else 'Not Loaded'}")
        st.write(f"- Validation: {'Completed' if st.session_state.has_validation else 'Pending'}")
        st.write(f"- Generation: {'Completed' if st.session_state.has_generated else 'Pending'}")
    
    # Upload Excel page
    elif page == "Upload Excel":
        st.subheader("Upload Excel File")
        st.write("Upload your Excel file with Consol PL and Consol BS sheets.")
        
        uploaded_file = st.file_uploader("Choose Excel file", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process Excel
                processor = ExcelProcessor(tmp_path)
                pl_data = processor.extract_pl_data()
                bs_data = processor.extract_bs_data()
                
                # Store data in session state
                st.session_state.excel_pl_data = pl_data
                st.session_state.excel_bs_data = bs_data
                st.session_state.excel_filename = uploaded_file.name
                
                # Mark as loaded
                st.session_state.has_excel = True
                
                st.success(f"Excel loaded successfully from {uploaded_file.name}")
                
                # Show data
                st.write("### P&L Data:")
                st.json(pl_data)
                st.write("### Balance Sheet Data:")
                st.json(bs_data)
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as error:
                st.error(f"Error processing Excel file: {str(error)}")
    
    # Upload PDF page
    elif page == "Upload PDF":
        st.subheader("Upload PDF File")
        st.write("Upload your prior year financial statements PDF.")
        
        uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
        
        if uploaded_file is not None:
            try:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process PDF
                parser = PDFParser(tmp_path)
                pdf_pl_data = parser.extract_income_statement_data()
                pdf_bs_data = parser.extract_balance_sheet_data()
                
                # Store data in session state
                st.session_state.pdf_pl_data = pdf_pl_data
                st.session_state.pdf_bs_data = pdf_bs_data
                st.session_state.pdf_filename = uploaded_file.name
                
                # Mark as loaded
                st.session_state.has_pdf = True
                
                st.success(f"PDF loaded successfully from {uploaded_file.name}")
                
                # Show data
                st.write("### PDF P&L Data:")
                st.json(pdf_pl_data)
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as error:
                st.error(f"Error processing PDF file: {str(error)}")
    
    # Validate page
    elif page == "Validate":
        st.subheader("Data Validation")
        
        if not st.session_state.has_excel:
            st.warning("Please upload Excel file first.")
        elif not st.session_state.has_pdf:
            st.warning("Please upload PDF file first.")
        else:
            st.success("Both files loaded. Ready for validation.")
            
            # Get entity information
            entity_name = st.text_input("Entity Name", value="Example Pty Ltd")
            current_year = st.number_input("Current Year", min_value=2020, max_value=2030, value=2025)
            
            if st.button("Run Validation"):
                try:
                    # Initialize validator
                    validator = FinancialStatementValidator(entity_name, current_year)
                    
                    # Run validation
                    is_valid, errors, warnings, queries = validator.validate_all(
                        bs_data=st.session_state.excel_bs_data,
                        pl_data=st.session_state.excel_pl_data,
                        prior_year_data=st.session_state.pdf_bs_data,
                        prior_re=0,
                        directors=[{'name': 'Test', 'title': 'Director'}],
                        compiler={'name': 'Test', 'title': 'CFO'},
                        tax_consolidation_entity="",
                        contingent_liability_text="",
                        notes_data={}
                    )
                    
                    # Store results
                    st.session_state.validation_errors = errors
                    st.session_state.validation_warnings = warnings
                    st.session_state.validation_passed = is_valid
                    
                    # Mark as validated
                    st.session_state.has_validation = True
                    
                    # Show results
                    if errors:
                        st.error("Validation Errors:")
                        for error in errors:
                            st.write(f"- {error}")
                    
                    if warnings:
                        st.warning("Validation Warnings:")
                        for warning in warnings:
                            st.write(f"- {warning}")
                    
                    if is_valid and not warnings:
                        st.success("All validations passed!")
                
                except Exception as error:
                    st.error(f"Validation error: {str(error)}")
    
    # Generate page
    elif page == "Generate":
        st.subheader("Generate Financial Statements")
        
        if not st.session_state.has_excel:
            st.warning("Please upload Excel file first.")
        elif not st.session_state.has_pdf:
            st.warning("Please upload PDF file first.")
        elif not st.session_state.has_validation:
            st.warning("Please run validation first.")
        else:
            st.success("Ready to generate statements!")
            
            # Entity information
            entity_name = st.text_input("Entity Name", value="Example Pty Ltd")
            current_year = st.number_input("Current Year", min_value=2020, max_value=2030, value=2025)
            
            if st.button("Generate PDF"):
                try:
                    with st.spinner("Generating PDF..."):
                        # Create generator
                        generator = AASBFinancialStatementGenerator(
                            entity_name,
                            current_year,
                            st.session_state.pdf_bs_data
                        )
                        
                        # Generate statements
                        filename = generator.generate_financial_statements(
                            st.session_state.excel_pl_data,
                            st.session_state.excel_bs_data,
                            {},
                            [{'name': 'Test Director', 'title': 'Director'}],
                            {'name': 'Test Compiler', 'title': 'CFO'}
                        )
                        
                        # Store filename
                        st.session_state.generated_filename = filename
                        
                        # Mark as generated
                        st.session_state.has_generated = True
                        
                        st.success(f"PDF generated: {filename}")
                        
                        # Download button
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="Download PDF",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="application/pdf"
                            )
                
                except Exception as error:
                    st.error(f"Generation error: {str(error)}")
                    import traceback
                    st.code(traceback.format_exc())

except Exception as main_error:
    st.error(f"Application Error: {str(main_error)}")
    import traceback
    st.code(traceback.format_exc())
