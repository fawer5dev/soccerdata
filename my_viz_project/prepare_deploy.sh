#!/bin/bash

# 🚀 Prepare Project for Deployment
# ==================================

echo "🎯 Preparing your project for deployment..."
echo ""

cd "$(dirname "$0")"

# Check if files exist
echo "✅ Checking required files..."
files=("web_app.py" "requirements.txt" ".gitignore" ".streamlit/config.toml")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file - MISSING!"
    fi
done

echo ""
echo "📦 Files ready for deployment:"
echo ""
ls -lh web_app.py requirements.txt .gitignore 2>/dev/null | awk '{print "   ", $9, "("$5")"}'
echo ""

echo "📋 NEXT STEPS:"
echo ""
echo "1. Create GitHub repository:"
echo "   https://github.com/new"
echo ""
echo "2. Upload these files to GitHub:"
echo "   - web_app.py"
echo "   - requirements.txt"
echo "   - .gitignore"
echo "   - .streamlit/config.toml"
echo ""
echo "3. Deploy on Streamlit Cloud:"
echo "   https://streamlit.io/cloud"
echo ""
echo "4. Share your app URL with the world! 🌍"
echo ""
echo "📖 Full guide: DEPLOYMENT_GUIDE.md"
echo ""
