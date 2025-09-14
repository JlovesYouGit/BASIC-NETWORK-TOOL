#!/usr/bin/env python3
"""
Test script for improved network blocking functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.manager import DeviceManager

def test_improved_blocking():
    """Test the improved network blocking functionality"""
    print("Testing Improved Network Blocking Functionality...")
    
    # Create a DeviceManager instance
    manager = DeviceManager()
    
    # Test blocking an unreachable device
    print("\n1. Testing blocking of unreachable device...")
    test_ip = "23.192.228.80"  # This IP is likely unreachable
    print(f"Attempting to block device {test_ip}...")
    result = manager.block_device_network_access(test_ip)
    print(f"Blocking device {test_ip}: {'SUCCESS' if result else 'FAILED'}")
    
    # Test unblocking an unreachable device
    print("\n2. Testing unblocking of unreachable device...")
    print(f"Attempting to unblock device {test_ip}...")
    result = manager.unblock_device_network_access(test_ip)
    print(f"Unblocking device {test_ip}: {'SUCCESS' if result else 'FAILED'}")
    
    # Test with a different IP
    print("\n3. Testing with different IP...")
    test_ip2 = "192.168.1.200"
    print(f"Attempting to block device {test_ip2}...")
    result = manager.block_device_network_access(test_ip2)
    print(f"Blocking device {test_ip2}: {'SUCCESS' if result else 'FAILED'}")
    
    print(f"Attempting to unblock device {test_ip2}...")
    result = manager.unblock_device_network_access(test_ip2)
    print(f"Unblocking device {test_ip2}: {'SUCCESS' if result else 'FAILED'}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_improved_blocking()