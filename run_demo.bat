@echo off
echo ===================================================
echo   API Vigilance Tool - Quick Demo
echo ===================================================
echo.
echo [1/3] Installing/Verifying Dependencies...
pip install -r requirements.txt > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies. Please ensure Python is installed.
    pause
    exit /b
)
echo Dependencies OK.
echo.

echo [2/3] Running Tool on Sample Data...
echo Compared: tests/sample_old.yaml vs tests/sample_new.yaml
echo.
python -m src.main --old tests/sample_old.yaml --new tests/sample_new.yaml
echo.

echo [3/3] Running Automated Checks...
python src/qa.py
echo.

echo ===================================================
echo   Demo Complete!
echo ===================================================
pause
