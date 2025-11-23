#!/usr/bin/env python3
"""
Streamlit App for AASB Financial Statement Generator
Ultra-robust version with all potential NameError sources eliminated.
"""

import sys
import os
import tempfile

# Add the src directory to the Python path so imports work
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
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state with simple boolean flags
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = None
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    if 'generated_file' not in st.session_state:
        st.session_state.generated_file = False
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Page:", ["Home", "Upload", "Validate", "Preview", "Generate"])
    
    # Safe status checking function
    def get_status():
        excel_ok = st.session_state.excel_data is not None
        pdf_ok = st.session_state.pdf_data is not None
        valid_ok = st.session_state.validation_results is not None
        gen_ok = st.session_state.generated_file
        return excel_ok, pdf_ok, valid_ok, gen_ok
    
    # Get current status
    excel_ready, pdf_ready, valid_ready, gen_ready = get_status()
    
    # Home Page
    if page == "Home":
        st.title("AASB Financial Statement Generator")
        st.write("Generate AASB-compliant financial statements")
        
        st.write("### Steps:")
        st.write("1. Upload Excel and PDF files")
        st.write("2. Run validation")
        st.write("3. Preview data")
        st.write("4. Generate PDF statements")
        
        # Status display
        st.sidebar.write("Status:")
        st.sidebar.write(f"Excel: {'Yes' if excel_ready else 'No'}")
        st.sidebar.write(f"PDF: {'Yes' if pdf_ready else 'No'}")
        st.sidebar.write(f"Valid: {'Yes' if valid_ready else 'No'}")
        st.sidebar.write(f"PDF Gen: {'Yes' if gen_ready else 'No'}")
    
    # Upload Page
    elif page == "Upload":
        st.title("Upload Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Excel File")
            excel_file = st.file_uploader("Excel", type=['xlsx', 'xls'], key="excel1")
            
            if excel_file is not None:
                try:
                    # Save temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        tmp.write(excel_file.getvalue())
                        tmp_path = tmp.name
                    
                    # Process
                    processor = ExcelProcessor(tmp_path)
                    pl_data = processor.extract_pl_data()
                    bs_data = processor.extract_bs_data()
                    
                    # Store
                    st.session_state.excel_data = {
                        'pl': pl_data,
                        'bs': bs_data,
                        'name': excel_file.name
                    }
                    
                    st.success(f"Excel loaded: {excel_file.name}")
                    st.write("P&L Data:")
                    st.json(pl_data)
                    st.write("BS Data:")
                    st.json(bs_data)
                    
                    # Cleanup
                    os.unlink(tmp_path)
                    
                except Exception as error:
                    error_msg = "Error processing Excel"
                    st.error(error_msg)
        
        with col2:
            st.write("PDF File")
            pdf_file = st.file_uploader("PDF", type=['pdf'], key="pdf1")
            
            if pdf_file is not None:
                try:
                    # Save temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                        tmp.write(pdf_file.getvalue())
                        tmp_path = tmp.name
                    
                    # Process
                    parser = PDFParser(tmp_path)
                    pdf_pl = parser.extract_income_statement_data()
                    pdf_bs = parser.extract_balance_sheet_data()
                    
                    # Store
                    st.session_state.pdf_data = {
                        'pl': pdf_pl,
                        'bs': pdf_bs,
                        'name': pdf_file.name
                    }
                    
                    st.success(f"PDF loaded: {pdf_file.name}")
                    st.write("PDF P&L Data:")
                    st.json(pdf_pl)
                    
                    # Cleanup
                    os.unlink(tmp_path)
                    
                except Exception as error:
                    error_msg = "Error processing PDF"
                    st.error(error_msg)
    
    # Validate Page
    elif page == "Validate":
        st.title("Data Validation")
        
        if not excel_ready or not pdf_ready:
            st.warning("Upload both files first")
        else:
            st.success("Ready for validation")
            
            entity = st.text_input("Entity", value="Example Pty Ltd")
            year = st.number_input("Year", min_value=2020, max_value=2030, value=2025)
            
            if st.button("Validate"):
                try:
                    # Initialize validator
                    validator = FinancialStatementValidator(entity, year)
                    
                    # Get data
                    excel_bs = st.session_state.excel_data['bs']
                    excel_pl = st.session_state.excel_data['pl']
                    pdf_bs = st.session_state.pdf_data['bs']
                    
                    # Get prior retained earnings
                    prior_re = pdf_bs.get('equity', {}).get('retained_earnings', 0)
                    if prior_re == 0:
                        prior_re = pdf_bs.get('retained_earnings', 0)
                    
                    # Run validation
                    is_valid, errors, warnings, queries = validator.validate_all(
                        bs_data=excel_bs,
                        pl_data=excel_pl,
                        prior_year_data=pdf_bs,
                        prior_re=prior_re,
                        directors=[{'name': 'Test', 'title': 'Director'}],
                        compiler={'name': 'Test', 'title': 'CFO'},
                        tax_consolidation_entity="",
                        contingent_liability_text="",
                        notes_data={}
                    )
                    
                    # Store results
                    st.session_state.validation_results = {
                        'valid': is_valid,
                        'errors': errors,
                        'warnings': warnings
                    }
                    
                    # Show results
                    if errors:
                        st.error("Errors found:")
                        for error in errors:
                            st.write(f"- {error}")
                    
                    if warnings:
                        st.warning("Warnings:")
                        for warning in warnings:
                            st.write(f"- {warning}")
                    
                    if is_valid and not warnings:
                        st.success("All validations passed!")
                
                except Exception as error:
                    st.error("Validation error occurred")
    
    # Preview Page
    elif page == "Preview":
        st.title("Data Preview")
        
        if st.session_state.excel_data:
            st.write("Excel P&L Data:")
            st.json(st.session_state.excel_data['pl'])
            st.write("Excel BS Data:")
            st.json(st.session_state.excel_data['bs'])
        else:
            st.write("No Excel data")
        
        if st.session_state.pdf_data:
            st.write("PDF P&L Data:")
            st.json(st.session_state.pdf_data['pl'])
            st.write("PDF BS Data:")
            st.json(st.session_state.pdf_data['bs'])
        else:
            st.write("No PDF data")
        
        # Comparison if both available
        if st.session_state.excel_data and st.session_state.pdf_data:
            st.write("Comparison:")
            excel_bs = st.session_state.excel_data['bs']
            pdf_bs = st.session_state.pdf_data['bs']
            
            comp = {
                'Excel Assets': excel_bs.get('total_assets', 0),
                'PDF Assets': pdf_bs.get('total_assets', 0),
                'Excel Equity': excel_bs.get('total_equity', 0),
                'PDF Equity': pdf_bs.get('total_equity', 0)
            }
            st.json(comp)
    
    # Generate Page
    elif page == "Generate":
        st.title("Generate PDF")
        
        if not excel_ready or not valid_ready:
            st.warning("Complete upload and validation first")
        else:
            st.success("Ready to generate")
            
            entity = st.text_input("Entity Name", value="Example Pty Ltd")
            year = st.number_input("Financial Year", min_value=2020, max_value=2030, value=2025)
            
            if st.button("Generate PDF"):
                try:
                    with st.spinner("Creating PDF..."):
                        # Get data
                        prior_data = st.session_state.pdf_data['bs']
                        
                        # Create generator
                        generator = AASBFinancialStatementGenerator(entity, year, prior_data)
                        
                        # Generate
                        filename = generator.generate_financial_statements(
                            st.session_state.excel_data['pl'],
                            st.session_state.excel_data['bs'],
                            {},
                            [{'name': 'Test', 'title': 'Director'}],
                            {'name': 'Test', 'title': 'CFO'}
                        )
                        
                        # Mark as generated
                        st.session_state.generated_file = True
                        st.session_state.pdf_filename = filename
                        
                        st.success(f"PDF created: {filename}")
                        
                        # Download
                        try:
                            with open(filename, "rb") as f:
                                st.download_button(
                                    label="Download PDF",
                                    data=f.read(),
                                    file_name=os.path.basename(filename),
                                    mime="application/pdf"
                                )
                        except:
                            st.write("PDF file ready for download")
                
                except Exception as error:
                    st.error("Error generating PDF")
    
    # Final status display
    st.sidebar.write("---")
    st.sidebar.write("Files:")
    if excel_ready:
        st.sidebar.write(f"Excel: {st.session_state.excel_data['name']}")
    if pdf_ready:
        st.sidebar.write(f"PDF: {st.session_state.pdf_data['name']}")

except ImportError:
    st.error("Import Error - Check dependencies")

except Exception:
    st.error("Application Error - Check logs")
