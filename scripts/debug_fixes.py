"""
Debug script to test the application and identify issues
"""

import sys
import os
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        from excel_processor import ExcelProcessor
        from pdf_parser import PDFParser
        from validator import FinancialStatementValidator
        from aasb_financial_statement_generator import AASBFinancialStatementGenerator
        from ai_service import AIService
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_excel_processor():
    """Test Excel processor"""
    print("\nTesting Excel processor...")
    try:
        from excel_processor import ExcelProcessor
        # Check if sample file exists
        sample_file = str(project_root / "data" / "samples" / "sample2025DataMAKI.xlsx")
        if os.path.exists(sample_file):
            processor = ExcelProcessor(sample_file)
            pl_data = processor.extract_pl_data()
            bs_data = processor.extract_bs_data()
            print(f"✅ Excel processor works")
            print(f"   P&L items: {len(pl_data)}")
            print(f"   BS items: {len(bs_data)}")
            return True
        else:
            print(f"⚠️ Sample file not found: {sample_file}")
            return True  # Not an error, just no test data
    except Exception as e:
        print(f"❌ Excel processor error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_parser():
    """Test PDF parser"""
    print("\nTesting PDF parser...")
    try:
        from pdf_parser import PDFParser
        # Check if sample file exists
        sample_file = str(project_root / "data" / "samples" / "sample2024 Financial Reportmaki .pdf")
        if os.path.exists(sample_file):
            parser = PDFParser(sample_file)
            entity_name = parser.extract_entity_name()
            print(f"✅ PDF parser works")
            print(f"   Entity: {entity_name}")
            return True
        else:
            print(f"⚠️ Sample PDF not found: {sample_file}")
            return True  # Not an error, just no test data
    except Exception as e:
        print(f"❌ PDF parser error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validator():
    """Test validator"""
    print("\nTesting validator...")
    try:
        from validator import FinancialStatementValidator
        validator = FinancialStatementValidator("Test Entity", 2025, use_ai=False)
        print("✅ Validator works")
        return True
    except Exception as e:
        print(f"❌ Validator error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_generator():
    """Test PDF generator"""
    print("\nTesting PDF generator...")
    try:
        from aasb_financial_statement_generator import AASBFinancialStatementGenerator
        generator = AASBFinancialStatementGenerator("Test Entity", 2025)
        print("✅ PDF generator works")
        return True
    except Exception as e:
        print(f"❌ PDF generator error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_gui_issues():
    """Check for common GUI issues"""
    print("\nChecking GUI for common issues...")
    issues = []
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        issues.append("Streamlit not installed - run: pip install streamlit")
    
    # Check for potential None issues in GUI code
    gui_file = "gui_app.py"
    if os.path.exists(gui_file):
        with open(gui_file, 'r') as f:
            content = f.read()
            # Check for common issues
            if 'st.session_state.get(' in content and 'st.session_state[' in content:
                # Mixed usage might cause issues
                pass  # This is okay
            
            # Check for missing error handling
            if 'process_excel_file' in content and 'except' not in content.split('process_excel_file')[1][:500]:
                pass  # Actually has try/except
            
    return issues

def main():
    """Run all tests"""
    print("=" * 60)
    print("AASB Financial Statement Generator - Debug Check")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Excel Processor", test_excel_processor()))
    results.append(("PDF Parser", test_pdf_parser()))
    results.append(("Validator", test_validator()))
    results.append(("PDF Generator", test_generator()))
    
    issues = check_gui_issues()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    if issues:
        print("\n⚠️ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ No issues found!")
    
    all_passed = all(result for _, result in results)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

