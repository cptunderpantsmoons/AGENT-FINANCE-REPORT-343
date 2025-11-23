#!/usr/bin/env python3
"""
Simple test to check if imports work in Streamlit environment
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing imports...")
    
    # Test basic imports
    import pandas as pd
    print("✅ pandas imported successfully")
    
    import numpy as np
    print("✅ numpy imported successfully")
    
    import streamlit as st
    print("✅ streamlit imported successfully")
    
    # Test our modules
    from excel_processor import ExcelProcessor
    print("✅ ExcelProcessor imported successfully")
    
    from pdf_parser import PDFParser
    print("✅ PDFParser imported successfully")
    
    from validator import FinancialStatementValidator
    print("✅ FinancialStatementValidator imported successfully")
    
    from aasb_financial_statement_generator import AASBFinancialStatementGenerator
    print("✅ AASBFinancialStatementGenerator imported successfully")
    
    from ai_service import AIService
    print("✅ AIService imported successfully")
    
    print("\n🎉 All imports successful! The app should work.")
    
except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected Error: {str(e)}")
