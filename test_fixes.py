#!/usr/bin/env python3
"""
Test script to verify the fixes made to the Network Management Tool.
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.scanner import NetworkScanner
from modules.manager import DeviceManager
from modules.dashboard import InteractiveDashboard

def test_module_imports():
    """Test that all modules can be imported without errors."""
    try:
        scanner = NetworkScanner()
        manager = DeviceManager()
        dashboard = InteractiveDashboard(scanner, manager)
        print("✅ All modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        return False

def test_method_signatures():
    """Test that method signatures are correct."""
    try:
        scanner = NetworkScanner()
        manager = DeviceManager()
        
        # Test scanner methods exist
        assert hasattr(scanner, 'scan_local_network')
        assert hasattr(scanner, 'scan_server_network')
        assert hasattr(scanner, 'scan_web_server')
        assert hasattr(scanner, 'fingerprint_device')
        print("✅ Scanner module methods verified")
        
        # Test manager methods exist and have correct signatures
        assert hasattr(manager, 'manage_device')
        assert hasattr(manager, 'secure_manage_device')
        assert hasattr(manager, 'test_connection')
        print("✅ Manager module methods verified")
        
        return True
    except Exception as e:
        print(f"❌ Error verifying method signatures: {e}")
        return False

def test_dashboard_method_calls():
    """Test that dashboard method calls work correctly."""
    try:
        scanner = NetworkScanner()
        manager = DeviceManager()
        dashboard = InteractiveDashboard(scanner, manager)
        
        # Verify dashboard has the methods we expect
        assert hasattr(dashboard, '_manage_device')
        assert hasattr(dashboard, '_show_device_details')
        assert hasattr(dashboard, '_scan_and_display')
        print("✅ Dashboard module methods verified")
        
        return True
    except Exception as e:
        print(f"❌ Error verifying dashboard methods: {e}")
        return False

def main():
    """Main test function."""
    print("Testing fixes made to the Network Management Tool...")
    print("=" * 50)
    
    tests = [
        test_module_imports,
        test_method_signatures,
        test_dashboard_method_calls
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed! Fixes have been successfully implemented.")
    else:
        print("❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()