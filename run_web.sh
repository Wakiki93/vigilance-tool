#!/bin/bash

echo "🚀 Starting API Vigilance Tool Web Interface..."
echo ""
echo "Installing dependencies (if needed)..."
pip install -q -r requirements.txt

echo ""
echo "✓ Dependencies installed"
echo ""
echo "🌐 Starting web server..."
echo "📍 Access the tool at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python web_app.py
