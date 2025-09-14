#!/usr/bin/env python3
"""
Test script for real network blocking functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.network_blocker import NetworkBlocker

def test_real_blocking():
    """Test the real network blocking functionality"""
    print("Testing Real Network Blocking Functionality...")
    
    # Create a NetworkBlocker instance
    blocker = NetworkBlocker()
    
    # Test with a test IP (using a private IP that shouldn't be in use)
    test_ip = "192.168.1.200"
    
    print(f"\n1. Testing blocking of IP {test_ip}...")
    print(f"Attempting to block IP {test_ip}...")
    result = blocker.block_ip(test_ip)
    print(f"Blocking IP {test_ip}: {'SUCCESS' if result else 'FAILED'}")
    
    # Check if IP is blocked
    is_blocked = blocker.is_ip_blocked(test_ip)
    print(f"IP {test_ip} is blocked: {is_blocked}")
    
    print(f"\n2. Testing unblocking of IP {test_ip}...")
    print(f"Attempting to unblock IP {test_ip}...")
    result = blocker.unblock_ip(test_ip)
    print(f"Unblocking IP {test_ip}: {'SUCCESS' if result else 'FAILED'}")
    
    # Check if IP is still blocked
    is_blocked = blocker.is_ip_blocked(test_ip)
    print(f"IP {test_ip} is blocked: {is_blocked}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_real_blocking()