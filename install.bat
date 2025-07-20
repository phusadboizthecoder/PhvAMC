@echo off
echo ============================================================
echo    AI Media Checker "PhvAMC" - Windows Installer
echo    Tien ich kiem tra noi dung AI chan that vl
echo    by PhvsadboizDEV
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found!

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install streamlit opencv-python tensorflow librosa pandas Pillow numpy

if %errorlevel% neq 0 (
    echo ERROR: Failed to install some dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo.
echo Starting AI Media Checker PhvAMC...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

REM Run the app
python -m streamlit run app.py --server.port 8501

pause