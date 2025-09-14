#!/usr/bin/env python3
"""
Test script to verify Nmap installation and python-nmap integration
"""

import nmap
import subprocess
import sys
import os

def test_nmap_executable():
    """Test if Nmap executable is accessible"""
    try:
        # Try to run nmap with full path first
        break_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'break')
        nmap_path = os.path.join(break_folder, 'nmap.exe')
        
        if os.path.exists(nmap_path):
            result = subprocess.run([nmap_path, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Nmap executable found and working (using full path)")
                print(result.stdout.split('\n')[0])  # Print just the first line
                return True, nmap_path
            else:
                print("❌ Nmap executable found but not working")
                print(f"Error: {result.stderr}")
                return False, None
        else:
            print("❌ Nmap executable not found in break folder")
            return False, None
    except Exception as e:
        print(f"❌ Error testing Nmap executable: {e}")
        return False, None

def test_python_nmap(nmap_path=None):
    """Test python-nmap library integration"""
    try:
        # If we have the nmap path, set it in the environment
        if nmap_path:
            nmap_dir = os.path.dirname(nmap_path)
            # Set the NMAP_PATH environment variable that python-nmap can use
            os.environ['NMAP_PATH'] = nmap_dir
            
        nm = nmap.PortScanner()
        print("✅ python-nmap library imported successfully")
        
        # Test basic functionality
        # Note: We won't actually scan anything here to avoid network activity
        print("✅ python-nmap PortScanner instantiated successfully")
        return True
    except nmap.PortScannerError as e:
        # Try with explicit path
        if nmap_path:
            try:
                nm = nmap.PortScanner(nmap_path)
                print("✅ python-nmap library imported successfully (with explicit path)")
                print("✅ python-nmap PortScanner instantiated successfully (with explicit path)")
                return True
            except Exception as e2:
                print(f"❌ Error testing python-nmap with explicit path: {e2}")
                return False
        else:
            print(f"❌ Error testing python-nmap: {e}")
            return False
    except Exception as e:
        print(f"❌ Error testing python-nmap: {e}")
        return False

def main():
    print("Testing Nmap installation and integration...")
    print("=" * 50)
    
    exe_result, nmap_path = test_nmap_executable()
    lib_result = False
    
    if exe_result:
        lib_result = test_python_nmap(nmap_path)
    
    print("\n" + "=" * 50)
    if exe_result and lib_result:
        print("🎉 All Nmap tests passed! The tool should work correctly.")
        return 0
    elif exe_result:
        print("✅ Nmap executable is working, but python-nmap integration needs configuration.")
        print("   The tool will use fallback methods when python-nmap fails.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())