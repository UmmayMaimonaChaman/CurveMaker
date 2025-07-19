#!/usr/bin/env python3
"""
CurveMaker - Startup Script
This script starts the Flask backend and opens the frontend in your default browser.
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask_cors', 'matplotlib', 'numpy', 'scipy', 'seaborn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting CurveMaker backend...")
    
    try:
        # Start the Flask app
        from app import app
        print("✅ Backend started successfully!")
        print("🌐 Backend URL: http://localhost:5000")
        return app
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def open_frontend():
    """Open the frontend in the default browser"""
    frontend_path = Path(__file__).parent / "index.html"
    
    if frontend_path.exists():
        print("🌐 Opening frontend in browser...")
        webbrowser.open(f'file://{frontend_path.absolute()}')
        print("✅ Frontend opened!")
    else:
        print("❌ index.html not found!")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🎨 CurveMaker - Professional Online Chart Maker")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start backend
    app = start_backend()
    if not app:
        sys.exit(1)
    
    # Wait a moment for backend to initialize
    time.sleep(2)
    
    # Open frontend
    if not open_frontend():
        sys.exit(1)
    
    print("\n🎉 CurveMaker is ready!")
    print("📊 Create beautiful charts and curves with ease!")
    print("\n💡 Tips:")
    print("   - Use the sample data buttons to get started quickly")
    print("   - Try different color schemes and grid styles")
    print("   - Export your charts as PNG or SVG")
    print("\n🛑 Press Ctrl+C to stop the server")
    
    try:
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using CurveMaker!")

if __name__ == "__main__":
    main() 