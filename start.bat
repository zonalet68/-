@echo off
chcp 65001 >nul
echo ========================================
echo      JW System Auto Login - GZIST
echo ========================================
echo.
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ first
    pause
    exit /b 1
)
echo OK: Python environment ready
echo.
echo Checking script files...
if not exist "jw.py" (
    echo ERROR: jw.py not found
    pause
    exit /b 1
)
if not exist "config.json" (
    echo ERROR: config.json not found
    pause
    exit /b 1
)
echo OK: Script files verified
echo.
echo Checking configuration...
python -c "import json; json.load(open('config.json', 'r', encoding='utf-8'))" >nul 2>&1
if errorlevel 1 (
    echo ERROR: config.json format is invalid
    pause
    exit /b 1
)
echo OK: Configuration verified
echo.
echo Starting JW System Auto Login...
echo ========================================
echo.
python jw.py
echo.
pause
