#!/usr/bin/env python3
"""
Test script for web API endpoints
"""

import requests
import time

def test_web_api():
    """Test the web API endpoints for network access control"""
    base_url = "http://localhost:5000"
    
    print("Testing Web API endpoints...")
    
    # Test blocking a device
    print("\n1. Testing device blocking endpoint...")
    try:
        response = requests.post(f"{base_url}/api/device/192.168.1.100/block", timeout=5)
        print(f"Block device response status: {response.status_code}")
        print(f"Block device response data: {response.json()}")
    except requests.exceptions.Timeout:
        print("Block device request timed out")
    except Exception as e:
        print(f"Error testing block endpoint: {e}")
    
    # Wait a moment
    time.sleep(1)
    
    # Test unblocking a device
    print("\n2. Testing device unblocking endpoint...")
    try:
        response = requests.post(f"{base_url}/api/device/192.168.1.100/unblock", timeout=5)
        print(f"Unblock device response status: {response.status_code}")
        print(f"Unblock device response data: {response.json()}")
    except requests.exceptions.Timeout:
        print("Unblock device request timed out")
    except Exception as e:
        print(f"Error testing unblock endpoint: {e}")
    
    print("\nWeb API tests completed!")

if __name__ == "__main__":
    test_web_api()