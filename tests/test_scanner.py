"""
Unit tests for the NetworkScanner module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.scanner import NetworkScanner

class TestNetworkScanner(unittest.TestCase):
    """Test cases for the NetworkScanner class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scanner = NetworkScanner()
    
    @patch('modules.scanner.srp')
    def test_scan_local_network(self, mock_srp):
        """Test scanning a local network."""
        # Mock the srp function to return a predefined result
        mock_result = [
            (MagicMock(), MagicMock(psrc='192.168.1.10', hwsrc='00:11:22:33:44:55')),
            (MagicMock(), MagicMock(psrc='192.168.1.11', hwsrc='aa:bb:cc:dd:ee:ff'))
        ]
        mock_srp.return_value = (mock_result, None)
        
        # Call the method under test
        devices = self.scanner.scan_local_network('192.168.1.0/24')
        
        # Assertions
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['ip'], '192.168.1.10')
        self.assertEqual(devices[0]['mac'], '00:11:22:33:44:55')
        self.assertEqual(devices[1]['ip'], '192.168.1.11')
        self.assertEqual(devices[1]['mac'], 'aa:bb:cc:dd:ee:ff')
    
    def test_fingerprint_device(self):
        """Test fingerprinting a device."""
        # Call the method under test
        device_info = self.scanner.fingerprint_device('192.168.1.10')
        
        # Assertions
        self.assertEqual(device_info['ip'], '192.168.1.10')
        self.assertEqual(device_info['os'], 'Unknown')
        self.assertEqual(device_info['hostname'], 'Unknown')
        self.assertIsInstance(device_info['ports'], list)

if __name__ == '__main__':
    unittest.main()