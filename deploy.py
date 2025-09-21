#!/usr/bin/env python3
"""
Deployment script for Resume Parser Backend
"""
import os
import sys
import subprocess
import shutil

def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ is required")
        return False
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("ERROR: Virtual environment not found. Run setup first.")
        return False
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("ERROR: .env file not found. Copy env_template.txt to .env and add your API key.")
        return False
    
    # Check if OpenAI API key is set
    with open(".env", "r") as f:
        content = f.read()
        if "your_openai_api_key_here" in content:
            print("ERROR: Please set your actual OpenAI API key in .env file")
            return False
    
    print("All requirements met!")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def test_service():
    """Test if the service starts correctly"""
    print("Testing service startup...")
    try:
        # Import the main module to check for syntax errors
        import main
        print("Service syntax check passed!")
        return True
    except Exception as e:
        print(f"ERROR: Service has syntax errors: {e}")
        return False

def create_startup_script():
    """Create startup script for production"""
    startup_script = """#!/bin/bash
# Resume Parser Backend Startup Script

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)

# Start the service
python main.py
"""
    
    with open("start.sh", "w") as f:
        f.write(startup_script)
    
    # Make it executable on Unix systems
    if os.name != 'nt':
        os.chmod("start.sh", 0o755)
    
    print("Startup script created: start.sh")

def main():
    """Main deployment function"""
    print("Resume Parser Backend - Deployment Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test service
    if not test_service():
        sys.exit(1)
    
    # Create startup script
    create_startup_script()
    
    print("\n" + "=" * 50)
    print("DEPLOYMENT SUCCESSFUL!")
    print("\nNext steps:")
    print("1. Ensure your OpenAI API key is set in .env file")
    print("2. Run: python main.py")
    print("3. Test the service: curl http://localhost:8000/health")
    print("4. For production, use: ./start.sh")
    print("\nFor React integration, see INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()
