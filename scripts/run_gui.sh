#!/bin/bash
# Script to run the Streamlit GUI application

echo "Starting AASB Financial Statement Generator GUI..."
echo ""

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run Streamlit app
streamlit run src/gui_app.py --server.port 8501 --server.address localhost

