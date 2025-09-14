#!/usr/bin/env python3
"""
Simple Nmap integration test
"""

import os
import nmap

def test_nmap_with_explicit_path():
    """Test Nmap with explicit path to executable"""
    try:
        # Get the path to the break folder
        project_root = os.path.dirname(os.path.abspath(__file__))
        break_folder = os.path.join(project_root, '..', 'break')
        nmap_path = os.path.join(break_folder, 'nmap.exe')
        
        print(f"Looking for Nmap at: {nmap_path}")
        
        if os.path.exists(nmap_path):
            print("✅ Nmap executable found")
            
            # Try to create PortScanner with explicit path
            nm = nmap.PortScanner(nmap_path)
            print("✅ PortScanner created with explicit path")
            
            # Try a simple scan (localhost)
            print("Testing scan...")
            nm.scan('127.0.0.1', arguments='-sn')  # Simple ping scan
            
            hosts = nm.all_hosts()
            print(f"✅ Scan completed, found {len(hosts)} hosts")
            
            return True
        else:
            print("❌ Nmap executable not found")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Nmap Integration Test")
    print("=" * 20)
    
    success = test_nmap_with_explicit_path()
    
    if success:
        print("\n🎉 Nmap integration is working correctly!")
    else:
        print("\n⚠️  Nmap integration test failed.")