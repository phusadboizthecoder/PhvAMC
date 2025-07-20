#!/bin/bash

echo "============================================================"
echo "   AI Media Checker 'PhvAMC' - Linux/Mac Installer"
echo "   Tien ich kiem tra noi dung AI chan that vl"
echo "   by PhvsadboizDEV"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "Python found!"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install streamlit opencv-python tensorflow librosa pandas Pillow numpy

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install some dependencies"
    exit 1
fi

echo "Dependencies installed successfully!"
echo ""
echo "Starting AI Media Checker PhvAMC..."
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

# Run the app
python3 -m streamlit run app.py --server.port 8501