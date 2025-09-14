#!/usr/bin/env python3
"""
Run script for the Network Management Tool REST API
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web.api import create_api_app

if __name__ == '__main__':
    app = create_api_app()
    print("Starting Network Management Tool REST API...")
    print("API endpoints:")
    print("  GET  /api/scan/<local|server|web>")
    print("  GET  /api/device/<ip>/fingerprint")
    print("  POST /api/device/<ip>/manage")
    print("Access the API at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)