#!/usr/bin/env python3
"""
Run script for the Network Management Tool Web Interface
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web.app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting Network Management Tool Web Interface...")
    print("Access the dashboard at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)