#!/bin/bash

# 🌐 Launch Soccer Data Web App
# =============================

echo "🚀 Starting Soccer Team Evolution Web App..."
echo ""

cd "$(dirname "$0")"

# Activate virtual environment
source ../venv_soccer_viz/bin/activate

# Check if streamlit is installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing Streamlit..."
    pip install streamlit
fi

echo "✅ Environment ready!"
echo ""
echo "🌐 Launching web app..."
echo "   Your browser will open automatically"
echo "   Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
streamlit run web_app.py
