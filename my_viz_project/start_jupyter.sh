#!/bin/bash

# ⚽ Soccer Data Visualization Project - Setup Script
# ==================================================

echo "⚽ Setting up Soccer Data Visualization Environment..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")/.."

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv_soccer_viz/bin/activate

# Verify installation
echo "✅ Checking installed packages..."
python -c "import soccerdata; import matplotlib; import seaborn; import plotly" && echo "   All packages OK!" || echo "   ⚠️  Some packages missing!"

# Start Jupyter Notebook
echo ""
echo "🚀 Starting Jupyter Notebook..."
echo "   Navigate to: my_viz_project/notebooks/"
echo "   Press Ctrl+C to stop the server"
echo ""

jupyter notebook my_viz_project/notebooks/

# Deactivate when done
# deactivate
