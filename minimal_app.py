#!/usr/bin/env python3
"""
Minimal Streamlit App for Testing
Simple version to test if the basic app structure works.
"""

import sys
import os

# Add the src directory to the Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import from our package
try:
    # Test basic imports first
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    # Test our imports
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
    
    # Main app
    st.title("📊 AASB Financial Statement Generator")
    st.write("Generate AASB-compliant financial statements for non-reporting entities")
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose:", ["Home", "Test Imports", "Upload Test"])
    
    if page == "Home":
        st.success("✅ App loaded successfully!")
        st.write("""
        The app is working correctly. You can now:
        1. Upload Excel files for processing
        2. Upload PDF files for parsing
        3. Generate financial statements
        """)
        
        # Show available modules
        st.subheader("Available Components:")
        st.write("- ✅ ExcelProcessor")
        st.write("- ✅ PDFParser") 
        st.write("- ✅ FinancialStatementValidator")
        st.write("- ✅ AASBFinancialStatementGenerator")
        
    elif page == "Test Imports":
        st.subheader("Import Test Results")
        st.write("All required modules imported successfully!")
        
    elif page == "Upload Test":
        st.subheader("File Upload Test")
        uploaded_file = st.file_uploader("Test file upload", type=['xlsx', 'pdf'])
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
    
except ImportError as e:
    st.error(f"❌ Import Error: {str(e)}")
    st.write("Please check the requirements and package structure.")
    
except Exception as e:
    st.error(f"❌ Unexpected Error: {str(e)}")
    st.write("An error occurred. Please check the logs.")
    import traceback
    st.code(traceback.format_exc())
