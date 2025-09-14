#!/usr/bin/env python3
"""
Test script for enhanced SSH key auto-detection functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.manager import DeviceManager

def test_enhanced_ssh_key_detection():
    """Test the enhanced SSH key auto-detection functionality."""
    print("Testing enhanced SSH key auto-detection...")
    
    # Create a device manager instance
    manager = DeviceManager()
    
    # Test with localhost
    test_ip = "127.0.0.1"
    print(f"\nTesting with IP: {test_ip}")
    
    # Create mock device info (as if from fingerprinting)
    device_info = {
        'ip': test_ip,
        'hostname': 'localhost',
        'os': 'Linux Ubuntu 20.04',
        'ports': [{'port': 22, 'service': 'ssh', 'version': 'OpenSSH 8.2'}]
    }
    
    print(f"Device info: {device_info}")
    
    # Test hostname resolution
    hostname = manager._resolve_hostname(test_ip)
    print(f"Resolved hostname: {hostname}")
    
    # Test SSH key path generation with device info
    key_paths = manager._get_ssh_key_paths(test_ip, hostname, device_info)
    print(f"Potential key paths: {key_paths}")
    
    # Test auto-detection with device info
    detected_key = manager._detect_ssh_key_for_device(test_ip, device_info)
    print(f"Auto-detected key: {detected_key}")
    
    # Test secure_manage_device with device info
    print("\nTesting secure_manage_device with device info...")
    # This would normally connect to the device, but we'll just test the key detection part
    # manager.secure_manage_device(test_ip, None, 'admin', device_info)

if __name__ == "__main__":
    test_enhanced_ssh_key_detection()