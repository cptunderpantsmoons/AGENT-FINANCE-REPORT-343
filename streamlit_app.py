#!/usr/bin/env python3
"""
Streamlit App Entry Point for AASB Financial Statement Generator
This file serves as the main entry point for Streamlit deployment.
"""

import sys
import os

# Add the src directory to the Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import from our package
try:
    from src import ExcelProcessor, PDFParser, FinancialStatementValidator, AASBFinancialStatementGenerator, AIService
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    st.set_page_config(
        page_title="AASB Financial Statement Generator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 AASB Financial Statement Generator")
    st.write("Generate AASB-compliant financial statements for non-reporting entities")
    
    # Your Streamlit app code here
    st.success("✅ Application loaded successfully!")
    st.write("The import issue has been resolved. You can now build your Streamlit application.")
    
    # Example of how to use the imported classes:
    st.subheader("Available Components:")
    st.write("- ExcelProcessor: Process Excel financial data")
    st.write("- PDFParser: Parse prior year PDF statements")
    st.write("- FinancialStatementValidator: Validate financial data")
    st.write("- AASBFinancialStatementGenerator: Generate final statements")
    st.write("- AIService: AI-powered enhancements")
    
except ImportError as e:
    st.error(f"❌ Import Error: {str(e)}")
    st.write("There was an issue importing the required modules.")
    st.write("Please check that all dependencies are installed and the package structure is correct.")
    
except Exception as e:
    st.error(f"❌ Unexpected Error: {str(e)}")
    st.write("An unexpected error occurred. Please check the application logs.")
