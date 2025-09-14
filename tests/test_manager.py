"""
Unit tests for the DeviceManager module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import paramiko

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.manager import DeviceManager

class TestDeviceManager(unittest.TestCase):
    """Test cases for the DeviceManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = DeviceManager()
    
    @patch('modules.manager.paramiko')
    def test_manage_device_success(self, mock_paramiko):
        """Test successful device management with password authentication."""
        # Mock the SSH client and its methods
        mock_ssh_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        
        # Mock the exec_command return values
        mock_stdin = MagicMock()
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stderr.read.return_value.decode.return_value = ""
        mock_stdout.read.return_value.decode.return_value = "Command executed successfully"
        mock_ssh_client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)
        
        # Call the method under test
        self.manager.manage_device('192.168.1.10', 'admin', 'password123')
        
        # Assertions
        mock_paramiko.SSHClient.assert_called_once()
        mock_ssh_client.set_missing_host_key_policy.assert_called_once()
        mock_ssh_client.connect.assert_called_once_with(
            '192.168.1.10', username='admin', password='password123', timeout=10
        )
    
    @patch('modules.manager.paramiko')
    def test_manage_device_authentication_error(self, mock_paramiko):
        """Test device management with authentication error."""
        # Mock the SSH client to raise an authentication exception
        mock_ssh_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        mock_ssh_client.connect.side_effect = paramiko.AuthenticationException("Authentication failed")
        
        # Call the method under test
        self.manager.manage_device('192.168.1.10', 'admin', 'wrongpassword')
        
        # Assertions
        mock_paramiko.SSHClient.assert_called_once()
        mock_ssh_client.set_missing_host_key_policy.assert_called_once()
        mock_ssh_client.connect.assert_called_once_with(
            '192.168.1.10', username='admin', password='wrongpassword', timeout=10
        )
    
    @patch('modules.manager.paramiko')
    @patch('modules.manager.os.path.exists')
    def test_secure_manage_device_success(self, mock_exists, mock_paramiko):
        """Test successful device management with key authentication."""
        # Mock the file existence check
        mock_exists.return_value = True
        
        # Mock the SSH client and its methods
        mock_ssh_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        
        # Mock the RSAKey
        mock_rsa_key = MagicMock()
        mock_paramiko.RSAKey.from_private_key_file.return_value = mock_rsa_key
        
        # Mock the exec_command return values
        mock_stdin = MagicMock()
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stderr.read.return_value.decode.return_value = ""
        mock_stdout.read.return_value.decode.return_value = "Command executed successfully"
        mock_ssh_client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)
        
        # Call the method under test
        self.manager.secure_manage_device('192.168.1.10', '/path/to/key', 'admin')
        
        # Assertions
        mock_exists.assert_called_once_with('/path/to/key')
        mock_paramiko.SSHClient.assert_called_once()
        mock_ssh_client.set_missing_host_key_policy.assert_called_once()
        mock_paramiko.RSAKey.from_private_key_file.assert_called_once_with('/path/to/key')
    
    @patch('modules.manager.os.path.exists')
    def test_secure_manage_device_missing_key(self, mock_exists):
        """Test device management with missing key file."""
        # Mock the file existence check
        mock_exists.return_value = False
        
        # Call the method under test
        self.manager.secure_manage_device('192.168.1.10', '/path/to/missing/key', 'admin')
        
        # Assertions
        mock_exists.assert_called_once_with('/path/to/missing/key')
    
    @patch('modules.manager.paramiko')
    @patch('modules.manager.os.path.exists')
    def test_secure_manage_device_key_error(self, mock_exists, mock_paramiko):
        """Test device management with key authentication error."""
        # Mock the file existence check
        mock_exists.return_value = True
        
        # Mock the SSH client to raise an authentication exception
        mock_ssh_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        mock_paramiko.RSAKey.from_private_key_file.return_value = MagicMock()
        mock_ssh_client.connect.side_effect = paramiko.AuthenticationException("Key authentication failed")
        
        # Call the method under test
        self.manager.secure_manage_device('192.168.1.10', '/path/to/key', 'admin')
        
        # Assertions
        mock_exists.assert_called_once_with('/path/to/key')
        mock_paramiko.SSHClient.assert_called_once()
        mock_ssh_client.set_missing_host_key_policy.assert_called_once()

if __name__ == '__main__':
    unittest.main()