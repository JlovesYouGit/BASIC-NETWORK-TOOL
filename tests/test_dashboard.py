"""
Unit tests for the InteractiveDashboard module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.dashboard import InteractiveDashboard

class TestInteractiveDashboard(unittest.TestCase):
    """Test cases for the InteractiveDashboard class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock scanner and manager
        self.mock_scanner = MagicMock()
        self.mock_manager = MagicMock()
        
        # Create dashboard instance with mocks
        self.dashboard = InteractiveDashboard(self.mock_scanner, self.mock_manager)
    
    def test_initialization(self):
        """Test dashboard initialization."""
        # Assertions
        self.assertEqual(self.dashboard.scanner, self.mock_scanner)
        self.assertEqual(self.dashboard.manager, self.mock_manager)
        self.assertIsNotNone(self.dashboard.logger)
        self.assertIsNotNone(self.dashboard.console)
    
    @patch('modules.dashboard.Prompt')
    def test_scan_and_display_local_network(self, mock_prompt):
        """Test scanning and displaying local network devices."""
        # Mock the prompt to return 'back' to avoid interactive input
        mock_prompt.ask.return_value = 'back'
        
        # Mock the scanner to return some devices
        mock_devices = [
            {'ip': '192.168.1.10', 'mac': '00:11:22:33:44:55'},
            {'ip': '192.168.1.15', 'mac': 'aa:bb:cc:dd:ee:ff'}
        ]
        self.mock_scanner.scan_local_network.return_value = mock_devices
        
        # Call the method under test
        self.dashboard._scan_and_display('local')
        
        # Assertions
        self.mock_scanner.scan_local_network.assert_called_once()
    
    @patch('modules.dashboard.Prompt')
    def test_scan_and_display_server_network(self, mock_prompt):
        """Test scanning and displaying server network devices."""
        # Mock the prompt to return 'back' to avoid interactive input
        mock_prompt.ask.return_value = 'back'
        
        # Mock the scanner to return some devices
        mock_devices = [
            {'ip': '10.0.0.5', 'mac': '11:22:33:44:55:66'},
            {'ip': '10.0.0.10', 'mac': 'bb:cc:dd:ee:ff:00'}
        ]
        self.mock_scanner.scan_server_network.return_value = mock_devices
        
        # Call the method under test
        self.dashboard._scan_and_display('server')
        
        # Assertions
        self.mock_scanner.scan_server_network.assert_called_once()
    
    @patch('modules.dashboard.Prompt')
    def test_scan_and_display_web_server(self, mock_prompt):
        """Test scanning and displaying web server devices."""
        # Mock the prompt to return 'back' to avoid interactive input
        mock_prompt.ask.return_value = 'back'
        
        # Mock the scanner to return some devices
        mock_devices = [
            {'ip': '203.0.113.1', 'mac': '22:33:44:55:66:77'},
            {'ip': '203.0.113.2', 'mac': 'cc:dd:ee:ff:00:11'}
        ]
        self.mock_scanner.scan_web_server.return_value = mock_devices
        
        # Call the method under test
        self.dashboard._scan_and_display('web')
        
        # Assertions
        self.mock_scanner.scan_web_server.assert_called_once()
    
    def test_scan_and_display_invalid_network_type(self):
        """Test scanning with invalid network type."""
        # Call the method under test
        self.dashboard._scan_and_display('invalid')
        
        # Assertions
        self.mock_scanner.scan_local_network.assert_not_called()
        self.mock_scanner.scan_server_network.assert_not_called()
        self.mock_scanner.scan_web_server.assert_not_called()
    
    @patch('modules.dashboard.Prompt')
    def test_show_device_details(self, mock_prompt):
        """Test showing device details."""
        # Mock the prompt to return 'no' to avoid interactive input
        mock_prompt.ask.return_value = 'no'
        
        # Mock device information
        mock_device = {
            'ip': '192.168.1.10',
            'mac': '00:11:22:33:44:55',
            'hostname': 'test-host',
            'os': 'Linux',
            'ports': [
                {'port': 22, 'service': 'ssh', 'version': 'OpenSSH 7.9'},
                {'port': 80, 'service': 'http', 'version': 'Apache 2.4.41'}
            ]
        }
        
        # Call the method under test
        self.dashboard._show_device_details(mock_device)
        
        # No specific assertions needed as this is primarily a display method

if __name__ == '__main__':
    unittest.main()