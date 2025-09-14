"""
Unit tests for the enhanced dashboard module
"""

import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestEnhancedDashboard(unittest.TestCase):
    """Test cases for the enhanced dashboard module"""
    
    def test_enhanced_dashboard_import(self):
        """Test that the enhanced dashboard module can be imported"""
        try:
            from modules.enhanced_dashboard import EnhancedTerminalDashboard
            self.assertIsNotNone(EnhancedTerminalDashboard)
        except Exception as e:
            self.fail(f"Failed to import EnhancedTerminalDashboard: {e}")
    
    def test_enhanced_dashboard_initialization(self):
        """Test that the enhanced dashboard can be initialized"""
        try:
            from modules.enhanced_dashboard import EnhancedTerminalDashboard
            # Create mock scanner and manager
            class MockScanner:
                pass
            
            class MockManager:
                pass
            
            scanner = MockScanner()
            manager = MockManager()
            
            dashboard = EnhancedTerminalDashboard(scanner, manager)
            self.assertIsNotNone(dashboard)
        except Exception as e:
            self.fail(f"Failed to initialize EnhancedTerminalDashboard: {e}")

if __name__ == '__main__':
    unittest.main()