#!/usr/bin/env python3
"""
AI Media Checker "PhvAMC" - Launcher Script
Automatically checks and installs dependencies, then runs the app
"""

import subprocess
import sys
import os
import importlib.util

def check_package(package_name):
    """Check if a package is installed"""
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}")
        return False

def check_and_install_dependencies():
    """Check and install all required dependencies"""
    print("🔍 Checking dependencies for AI Media Checker PhvAMC...")
    
    # Required packages with their pip names
    dependencies = {
        'streamlit': 'streamlit',
        'cv2': 'opencv-python',
        'tensorflow': 'tensorflow',
        'librosa': 'librosa',
        'pandas': 'pandas',
        'PIL': 'Pillow',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    # Check each dependency
    for import_name, pip_name in dependencies.items():
        if not check_package(import_name):
            missing_packages.append(pip_name)
            print(f"❌ {pip_name} not found")
        else:
            print(f"✅ {pip_name} is installed")
    
    # Install missing packages
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            if not install_package(package):
                print(f"❌ Failed to install {package}")
                return False
        print("✅ All dependencies installed successfully!")
    else:
        print("✅ All dependencies are already installed!")
    
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['utils', '.streamlit']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'utils/media_detector.py',
        'utils/vietnamese_labels.py',
        '.streamlit/config.toml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease make sure all project files are in the same directory as this script.")
        return False
    
    print("✅ All required files found!")
    return True

def run_streamlit_app():
    """Run the Streamlit application"""
    print("\n🚀 Starting AI Media Checker PhvAMC...")
    print("📱 The app will open in your browser automatically")
    print("🌐 URL: http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running the application: {e}")

def main():
    """Main function to run the launcher"""
    print("=" * 60)
    print("🎯 AI Media Checker 'PhvAMC' Launcher")
    print("   Tiện ích kiểm tra nội dung AI chân thật vl")
    print("   by PhvsadboizDEV")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create directories
    create_directories()
    
    # Check required files
    if not check_required_files():
        sys.exit(1)
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("❌ Failed to install some dependencies")
        sys.exit(1)
    
    # Run the application
    run_streamlit_app()

if __name__ == "__main__":
    main()