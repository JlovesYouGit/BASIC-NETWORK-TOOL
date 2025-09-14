#!/usr/bin/env python3
"""
Test script for network access control functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.manager import DeviceManager

def test_network_access_control():
    """Test the network access control functionality"""
    print("Testing Network Access Control functionality...")
    
    # Create a DeviceManager instance
    manager = DeviceManager()
    
    # Test blocking a device
    print("\n1. Testing block_device_network_access...")
    test_ip = "192.168.1.100"
    result = manager.block_device_network_access(test_ip)
    print(f"Blocking device {test_ip}: {'SUCCESS' if result else 'FAILED'}")
    
    # Test unblocking a device
    print("\n2. Testing unblock_device_network_access...")
    result = manager.unblock_device_network_access(test_ip)
    print(f"Unblocking device {test_ip}: {'SUCCESS' if result else 'FAILED'}")
    
    # Test with a different IP
    print("\n3. Testing with different IP...")
    test_ip2 = "192.168.1.200"
    result = manager.block_device_network_access(test_ip2)
    print(f"Blocking device {test_ip2}: {'SUCCESS' if result else 'FAILED'}")
    
    result = manager.unblock_device_network_access(test_ip2)
    print(f"Unblocking device {test_ip2}: {'SUCCESS' if result else 'FAILED'}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_network_access_control()