"""
Unit tests for the web interface module
"""

import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestWebInterface(unittest.TestCase):
    """Test cases for the web interface module"""
    
    def test_app_creation(self):
        """Test that the Flask app can be created"""
        try:
            from web.app import create_app
            app = create_app()
            self.assertIsNotNone(app)
        except Exception as e:
            self.fail(f"Failed to create Flask app: {e}")
    
    def test_routes_exist(self):
        """Test that the expected routes are defined"""
        try:
            from web.app import create_app
            app = create_app()
            
            # Get all routes
            rules = [rule.rule for rule in app.url_map.iter_rules()]
            
            # Check that expected routes exist
            expected_routes = ['/', '/api/scan/local', '/api/scan/server', 
                             '/api/scan/web', '/api/device/<ip>/fingerprint']
            
            for route in expected_routes:
                self.assertIn(route, rules, f"Route {route} not found")
        except Exception as e:
            self.fail(f"Failed to check routes: {e}")

if __name__ == '__main__':
    unittest.main()