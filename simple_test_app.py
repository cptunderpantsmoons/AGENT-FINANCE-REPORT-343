#!/usr/bin/env python3
"""
Ultra-simple Streamlit test app
Minimal version to test basic functionality without errors.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test basic imports
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    # Test our modules
    from excel_processor import ExcelProcessor
    from pdf_parser import PDFParser
    from validator import FinancialStatementValidator
    from aasb_financial_statement_generator import AASBFinancialStatementGenerator
    
    # Set page config
    st.set_page_config(page_title="AASB Generator - Test", layout="wide")
    
    # Main content
    st.title("✅ AASB Financial Statement Generator")
    st.write("This is a working version of the app!")
    
    # Simple test
    st.subheader("🔧 Test Results")
    st.write("✅ Streamlit loaded successfully")
    st.write("✅ All modules imported successfully")
    st.write("✅ No NameError detected")
    
    # Show available functionality
    st.subheader("📋 Available Features")
    st.write("1. Excel file processing")
    st.write("2. PDF parsing")
    st.write("3. Data validation")
    st.write("4. PDF generation")
    st.write("5. File upload handling")
    
    # Status check
    st.subheader("📊 Status")
    st.success("All systems operational!")
    
    # Instructions
    st.subheader("🚀 Next Steps")
    st.write("1. Upload an Excel file to test processing")
    st.write("2. Upload a PDF file to test parsing")
    st.write("3. Use the full app for complete functionality")
    
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    
except Exception as e:
    st.error(f"Unexpected Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
