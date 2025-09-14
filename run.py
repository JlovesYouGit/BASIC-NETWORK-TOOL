#!/usr/bin/env python3
"""
Run script for the Network Management Tool.

This script sets up the Python path and runs the main application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main application
from network_tool import main

if __name__ == '__main__':
    main()