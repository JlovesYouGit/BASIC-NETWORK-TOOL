"""
Unit tests for the database utility module
"""

import unittest
import sys
import os
import tempfile
import json
import sqlite3

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestDatabase(unittest.TestCase):
    """Test cases for the database utility module"""
    
    def test_database_creation(self):
        """Test that the database can be created"""
        try:
            # Create a temporary database file for testing
            test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
            os.close(test_db_fd)  # Close the file descriptor immediately
            
            from utils.database import NetworkDatabase
            db = NetworkDatabase(test_db_path)
            self.assertIsNotNone(db)
            
            # Note: Not cleaning up temp file on Windows due to file locking issues
            # The OS will clean up temporary files eventually
        except Exception as e:
            self.fail(f"Failed to create database: {e}")
    
    def test_save_and_retrieve_device(self):
        """Test saving and retrieving a device"""
        try:
            # Create a temporary database file for testing
            test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
            os.close(test_db_fd)  # Close the file descriptor immediately
            
            from utils.database import NetworkDatabase
            db = NetworkDatabase(test_db_path)
            
            # Test device data
            device_data = {
                'ip': '192.168.1.100',
                'mac': '00:11:22:33:44:55',
                'hostname': 'test-device',
                'os': 'Linux',
                'ports': [
                    {'port': 22, 'service': 'ssh', 'version': 'OpenSSH 7.9'},
                    {'port': 80, 'service': 'http', 'version': 'Apache 2.4.41'}
                ]
            }
            
            # Save device
            device_id = db.save_device(device_data)
            self.assertIsNotNone(device_id)
            self.assertGreater(device_id, 0)
            
            # Retrieve device
            retrieved_device = db.get_device_by_ip('192.168.1.100')
            self.assertIsNotNone(retrieved_device)
            self.assertEqual(retrieved_device['ip'], '192.168.1.100')
            self.assertEqual(retrieved_device['mac'], '00:11:22:33:44:55')
            self.assertEqual(retrieved_device['hostname'], 'test-device')
            self.assertEqual(retrieved_device['os'], 'Linux')
            
            # Check that device info is properly stored and retrieved
            self.assertIn('ports', retrieved_device['device_info'])
            self.assertEqual(len(retrieved_device['device_info']['ports']), 2)
            
            # Note: Not cleaning up temp file on Windows due to file locking issues
            # The OS will clean up temporary files eventually
        except Exception as e:
            self.fail(f"Failed to save and retrieve device: {e}")
    
    def test_get_all_devices(self):
        """Test retrieving all devices"""
        try:
            # Create a temporary database file for testing
            test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
            os.close(test_db_fd)  # Close the file descriptor immediately
            
            from utils.database import NetworkDatabase
            db = NetworkDatabase(test_db_path)
            
            # Add multiple devices
            device1 = {'ip': '192.168.1.100', 'mac': '00:11:22:33:44:55', 'hostname': 'device1', 'os': 'Linux'}
            device2 = {'ip': '192.168.1.101', 'mac': '00:11:22:33:44:56', 'hostname': 'device2', 'os': 'Windows'}
            
            db.save_device(device1)
            db.save_device(device2)
            
            # Retrieve all devices
            devices = db.get_devices()
            self.assertEqual(len(devices), 2)
            
            # Check that devices are properly retrieved
            ip_addresses = [device['ip'] for device in devices]
            self.assertIn('192.168.1.100', ip_addresses)
            self.assertIn('192.168.1.101', ip_addresses)
            
            # Note: Not cleaning up temp file on Windows due to file locking issues
            # The OS will clean up temporary files eventually
        except Exception as e:
            self.fail(f"Failed to retrieve all devices: {e}")
    
    def test_save_scan_results(self):
        """Test saving scan results"""
        try:
            # Create a temporary database file for testing
            test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
            os.close(test_db_fd)  # Close the file descriptor immediately
            
            from utils.database import NetworkDatabase
            db = NetworkDatabase(test_db_path)
            
            # Test scan results
            scan_results = [
                {'ip': '192.168.1.100', 'mac': '00:11:22:33:44:55'},
                {'ip': '192.168.1.101', 'mac': '00:11:22:33:44:56'}
            ]
            
            # Save scan results
            scan_id = db.save_scan_results('local', scan_results)
            self.assertIsNotNone(scan_id)
            self.assertGreater(scan_id, 0)
            
            # Note: Not cleaning up temp file on Windows due to file locking issues
            # The OS will clean up temporary files eventually
        except Exception as e:
            self.fail(f"Failed to save scan results: {e}")
    
    def test_get_scan_history(self):
        """Test retrieving scan history"""
        try:
            # Create a temporary database file for testing
            test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
            os.close(test_db_fd)  # Close the file descriptor immediately
            
            from utils.database import NetworkDatabase
            db = NetworkDatabase(test_db_path)
            
            # Add multiple scan results
            scan1 = [{'ip': '192.168.1.100'}]
            scan2 = [{'ip': '192.168.1.101'}]
            
            db.save_scan_results('local', scan1)
            db.save_scan_results('server', scan2)
            
            # Retrieve scan history
            scans = db.get_scan_history()
            self.assertEqual(len(scans), 2)
            
            # Check that scan types are properly stored
            scan_types = [scan['scan_type'] for scan in scans]
            self.assertIn('local', scan_types)
            self.assertIn('server', scan_types)
            
            # Note: Not cleaning up temp file on Windows due to file locking issues
            # The OS will clean up temporary files eventually
        except Exception as e:
            self.fail(f"Failed to retrieve scan history: {e}")

if __name__ == '__main__':
    unittest.main()