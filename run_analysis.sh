#!/bin/bash

# 🚀 RUN YOUR TEAM EVOLUTION PROJECT
# ==================================

echo "🏆 Team Evolution Timeline - Quick Start"
echo "========================================"
echo ""
echo "This script will run your analysis and create beautiful charts!"
echo ""

# Check if we're in the right directory
if [ ! -d "my_viz_project" ]; then
    echo "❌ Error: Run this from the soccerdata directory"
    echo "   cd /Users/fawer5/Documents/fawer5dev/soccerdata"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv_soccer_viz/bin/activate

# Check if Python packages are installed
echo "✅ Checking packages..."
python -c "import soccerdata, matplotlib, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not found. Please run:"
    echo "   source venv_soccer_viz/bin/activate"
    echo "   pip install -e ."
    exit 1
fi

echo "✅ All packages OK!"
echo ""

# Run the demo
echo "🚀 Running Team Evolution Analysis..."
echo "   This will take 2-3 minutes to fetch data..."
echo ""

python my_viz_project/scripts/quick_demo.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "🎉 SUCCESS! Check your results:"
    echo "============================================"
    echo ""
    echo "📁 Output folder: my_viz_project/output/"
    echo ""
    echo "📊 Generated files:"
    ls -lh my_viz_project/output/*.png 2>/dev/null | awk '{print "   -", $9, "("$5")"}'
    echo ""
    echo "💡 Next steps:"
    echo "   1. Open the output folder to see your charts"
    echo "   2. Edit scripts/quick_demo.py to analyze different teams"
    echo "   3. Run this script again to regenerate"
    echo ""
    echo "⚽ Happy analyzing!"
else
    echo ""
    echo "❌ Error occurred. Check the output above for details."
fi
