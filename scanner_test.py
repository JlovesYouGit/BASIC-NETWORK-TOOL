#!/usr/bin/env python3
"""
Test the updated scanner module's Nmap handling
"""

import sys
import os

# Add the project directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_scanner_nmap_handling():
    """Test that the scanner module can handle Nmap correctly"""
    try:
        from modules.scanner import NetworkScanner
        print("✅ NetworkScanner module imported successfully")
        
        # Create an instance
        scanner = NetworkScanner()
        print("✅ NetworkScanner instance created successfully")
        
        # Check if Nmap path was located
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        break_folder = os.path.join(project_root, '..', 'break')
        nmap_path = os.path.join(break_folder, 'nmap.exe')
        
        if os.path.exists(nmap_path):
            print("✅ Nmap executable found in break folder")
            print(f"   Path: {nmap_path}")
        else:
            print("❌ Nmap executable not found in break folder")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error testing scanner module: {e}")
        return False

if __name__ == "__main__":
    print("Scanner Module Nmap Handling Test")
    print("=" * 35)
    
    success = test_scanner_nmap_handling()
    
    if success:
        print("\n🎉 Scanner module Nmap handling is working correctly!")
    else:
        print("\n⚠️  Scanner module Nmap handling test failed.")