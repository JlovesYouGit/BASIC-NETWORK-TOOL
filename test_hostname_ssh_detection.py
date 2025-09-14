#!/usr/bin/env python3
"""
Test script for hostname-based SSH key auto-detection functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.manager import DeviceManager
from modules.scanner import NetworkScanner

def test_hostname_ssh_key_detection():
    """Test the hostname-based SSH key auto-detection functionality."""
    print("Testing hostname-based SSH key auto-detection...")
    
    # Create a device manager instance
    manager = DeviceManager()
    
    # Test with localhost
    test_ip = "127.0.0.1"
    print(f"\nTesting with IP: {test_ip}")
    
    # Test hostname resolution
    hostname = manager._resolve_hostname(test_ip)
    print(f"Resolved hostname: {hostname}")
    
    # Test SSH key path generation with hostname
    key_paths = manager._get_ssh_key_paths(test_ip, hostname)
    print(f"Potential key paths based on hostname: {key_paths}")
    
    # Test auto-detection with hostname
    detected_key = manager._detect_ssh_key_for_device(test_ip, None)
    print(f"Auto-detected key: {detected_key}")
    
    # Test with device information (simulating what would come from fingerprinting)
    print("\nTesting with device information...")
    device_info = {
        'ip': test_ip,
        'hostname': hostname,  # This would be the actual hostname detected by the system
        'os': 'Linux Ubuntu 20.04',
        'ports': [{'port': 22, 'service': 'ssh', 'version': 'OpenSSH 8.2'}]
    }
    
    print(f"Device info: {device_info}")
    
    # Test SSH key path generation with device info
    key_paths_with_info = manager._get_ssh_key_paths(test_ip, hostname, device_info)
    print(f"Potential key paths with device info: {key_paths_with_info}")
    
    # Test auto-detection with device info
    detected_key_with_info = manager._detect_ssh_key_for_device(test_ip, device_info)
    print(f"Auto-detected key with device info: {detected_key_with_info}")

def test_actual_device_scanning():
    """Test with actual device scanning to see real hostname detection."""
    print("\n\nTesting with actual device scanning...")
    
    # Create scanner and manager instances
    scanner = NetworkScanner()
    manager = DeviceManager()
    
    # Scan local network (this will show real devices and their hostnames)
    print("Scanning local network...")
    devices = scanner.scan_local_network()
    
    if devices:
        print(f"Found {len(devices)} devices:")
        for i, device in enumerate(devices):
            ip = device['ip']
            mac = device.get('mac', 'Unknown')
            print(f"  {i+1}. IP: {ip}, MAC: {mac}")
            
            # Try to get detailed information for the first device
            if i == 0:
                print(f"  Getting detailed information for {ip}...")
                detailed_info = scanner.fingerprint_device(ip)
                print(f"  Detailed info: {detailed_info}")
                
                # Test SSH key detection with this real device info
                hostname = manager._resolve_hostname(ip)
                print(f"  Resolved hostname: {hostname}")
                
                key_paths = manager._get_ssh_key_paths(ip, hostname, detailed_info)
                print(f"  Potential key paths: {key_paths}")
                
                detected_key = manager._detect_ssh_key_for_device(ip, detailed_info)
                print(f"  Auto-detected key: {detected_key}")
    else:
        print("No devices found on local network.")

if __name__ == "__main__":
    test_hostname_ssh_key_detection()
    # Uncomment the next line to test with actual device scanning
    # test_actual_device_scanning()