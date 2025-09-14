"""
Unit tests for the REST API module
"""

import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestAPI(unittest.TestCase):
    """Test cases for the REST API module"""
    
    def test_api_creation(self):
        """Test that the Flask-RESTful API can be created"""
        try:
            from web.api import create_api_app
            app = create_api_app()
            self.assertIsNotNone(app)
        except Exception as e:
            self.fail(f"Failed to create Flask-RESTful API: {e}")
    
    def test_api_routes_exist(self):
        """Test that the expected API routes are defined"""
        try:
            from web.api import create_api_app
            app = create_api_app()
            
            # Get all routes
            rules = [rule.rule for rule in app.url_map.iter_rules()]
            
            # Check that expected routes exist
            expected_routes = ['/api/scan/<scan_type>', 
                             '/api/device/<ip_address>/fingerprint',
                             '/api/device/<ip_address>/manage']
            
            for route in expected_routes:
                self.assertIn(route, rules, f"Route {route} not found")
        except Exception as e:
            self.fail(f"Failed to check API routes: {e}")

if __name__ == '__main__':
    unittest.main()