@echo off
REM Comment Moderation System Setup Script for Windows

echo.
echo ==========================================
echo Comment Moderation System Setup
echo ==========================================
echo.

REM Check Python version
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo ✓ Dependencies installed
echo.

REM Load sample data
echo [5/5] Loading sample data...
python load_sample_data.py 50 >nul 2>&1
echo ✓ Sample data loaded (50 comments)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Starting application...
echo.
echo Access the application at:
echo   Dashboard:  http://localhost:5000/
echo   Analyzer:   http://localhost:5000/analyzer
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python run.py

pause
