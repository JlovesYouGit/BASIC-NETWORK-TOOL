#!/usr/bin/env python3
"""
Test script for MAC address handling functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.scanner import NetworkScanner
from modules.dashboard import InteractiveDashboard
from modules.enhanced_dashboard import EnhancedTerminalDashboard
from modules.manager import DeviceManager

def test_mac_address_handling():
    """Test MAC address handling in different scenarios."""
    print("Testing MAC address handling...")
    
    # Test with a device dictionary that has a MAC address
    device_with_mac = {
        'ip': '192.168.1.100',
        'mac': '00:11:22:33:44:55'
    }
    
    print(f"Device with MAC: {device_with_mac}")
    print(f"MAC address: {device_with_mac.get('mac', 'Unknown')}")
    
    # Test with a device dictionary that has no MAC address
    device_without_mac = {
        'ip': '192.168.1.101'
    }
    
    print(f"Device without MAC: {device_without_mac}")
    mac_address = device_without_mac.get('mac', 'Unknown')
    if not mac_address or mac_address == 'N/A':
        mac_address = 'Unknown'
    print(f"MAC address: {mac_address}")
    
    # Test with a device dictionary that has an empty MAC address
    device_with_empty_mac = {
        'ip': '192.168.1.102',
        'mac': ''
    }
    
    print(f"Device with empty MAC: {device_with_empty_mac}")
    mac_address = device_with_empty_mac.get('mac', 'Unknown')
    if not mac_address or mac_address == 'N/A':
        mac_address = 'Unknown'
    print(f"MAC address: {mac_address}")
    
    # Test with a device dictionary that has 'N/A' as MAC address
    device_with_na_mac = {
        'ip': '192.168.1.103',
        'mac': 'N/A'
    }
    
    print(f"Device with N/A MAC: {device_with_na_mac}")
    mac_address = device_with_na_mac.get('mac', 'Unknown')
    if not mac_address or mac_address == 'N/A':
        mac_address = 'Unknown'
    print(f"MAC address: {mac_address}")

def test_scanner_mac_handling():
    """Test how the scanner handles MAC addresses."""
    print("\n\nTesting scanner MAC address handling...")
    
    # Create a mock device list similar to what the scanner might return
    mock_devices = [
        {'ip': '192.168.1.1', 'mac': '00:11:22:33:44:55'},
        {'ip': '192.168.1.2'},  # No MAC
        {'ip': '192.168.1.3', 'mac': ''},  # Empty MAC
        {'ip': '192.168.1.4', 'mac': 'N/A'},  # N/A MAC
        {'ip': '192.168.1.5', 'mac': 'aa:bb:cc:dd:ee:ff'}
    ]
    
    print("Mock devices from scanner:")
    print("IP" + " "*18+"MAC")
    for device in mock_devices:
        mac_address = device.get('mac', 'Unknown')
        if not mac_address or mac_address == 'N/A':
            mac_address = 'Unknown'
        print(f"{device['ip']:<20} {mac_address}")

if __name__ == "__main__":
    test_mac_address_handling()
    test_scanner_mac_handling()