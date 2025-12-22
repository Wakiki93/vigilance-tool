#!/bin/bash
echo "==================================================="
echo "  API Vigilance Tool - Quick Demo (Linux/Mac)"
echo "==================================================="
echo ""

echo "[1/3] Installing/Verifying Dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Please ensure Python/pip is installed."
    exit 1
fi
echo "Dependencies OK."
echo ""

echo "[2/3] Running Tool on Sample Data..."
echo "Compared: tests/sample_old.yaml vs tests/sample_new.yaml"
echo ""
python3 -m src.main --old tests/sample_old.yaml --new tests/sample_new.yaml
echo ""

echo "[3/3] Running Automated Checks..."
python3 src/qa.py
echo ""

echo "==================================================="
echo "  Demo Complete!"
echo "==================================================="
read -p "Press enter to exit"
