#!/usr/bin/env python3
"""
Setup script for the Network Management Tool.

This script provides a simple way to install dependencies and set up the environment.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python dependencies."""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Python dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python dependencies: {e}")
        return False
    return True

def check_nmap():
    """Check if Nmap is installed on the system."""
    print("Checking for Nmap installation...")
    try:
        result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Nmap is already installed.")
            print(result.stdout.split('\n')[0])  # Print first line of version info
            return True
        else:
            print("Nmap is not installed or not in PATH.")
            print("Please download and install Nmap from https://nmap.org/download.html")
            return False
    except FileNotFoundError:
        print("Nmap is not installed or not in PATH.")
        print("Please download and install Nmap from https://nmap.org/download.html")
        return False

def main():
    """Main setup function."""
    print("Network Management Tool - Setup")
    print("=" * 40)
    
    # Install Python dependencies
    if not install_dependencies():
        print("Failed to install Python dependencies. Exiting.")
        sys.exit(1)
    
    # Check for Nmap
    nmap_installed = check_nmap()
    
    print("\nSetup completed!")
    if not nmap_installed:
        print("\nWarning: Nmap is required for advanced device fingerprinting.")
        print("Please install Nmap separately from https://nmap.org/download.html")
    
    print("\nTo run the tool:")
    print("  python run.py --help")
    print("\nFor more information, see the README.md file.")

if __name__ == "__main__":
    main()