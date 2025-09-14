#!/usr/bin/env python3
"""
Final verification script for the Network Management Tool
"""

import sys
import os
import subprocess

def test_module_imports():
    """Test that all modules can be imported successfully"""
    print("Testing module imports...")
    
    try:
        from src.modules.scanner import NetworkScanner
        print("✅ NetworkScanner module imported successfully")
    except Exception as e:
        print(f"❌ Error importing NetworkScanner: {e}")
        return False
    
    try:
        from src.modules.manager import DeviceManager
        print("✅ DeviceManager module imported successfully")
    except Exception as e:
        print(f"❌ Error importing DeviceManager: {e}")
        return False
    
    try:
        from src.modules.dashboard import InteractiveDashboard
        print("✅ InteractiveDashboard module imported successfully")
    except Exception as e:
        print(f"❌ Error importing InteractiveDashboard: {e}")
        return False
    
    return True

def test_dependencies():
    """Test that all dependencies are installed"""
    print("\nTesting dependencies...")
    
    dependencies = [
        'scapy',
        'paramiko',
        'nmap',
        'rich'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} installed successfully")
        except ImportError:
            print(f"❌ {dep} not installed")
            return False
    
    return True

def test_nmap_functionality():
    """Test Nmap functionality"""
    print("\nTesting Nmap functionality...")
    
    try:
        import nmap
        # Test with explicit path
        project_root = os.path.dirname(os.path.abspath(__file__))
        break_folder = os.path.join(project_root, '..', 'break')
        nmap_path = os.path.join(break_folder, 'nmap.exe')
        
        if os.path.exists(nmap_path):
            nm = nmap.PortScanner(nmap_path)
            print("✅ Nmap functionality working with explicit path")
            return True
        else:
            print("❌ Nmap executable not found in break folder")
            return False
    except Exception as e:
        print(f"❌ Error testing Nmap functionality: {e}")
        return False

def test_cli_help():
    """Test that CLI help works"""
    print("\nTesting CLI help...")
    
    try:
        result = subprocess.run([sys.executable, 'run.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ CLI help working")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing CLI help: {e}")
        return False

def main():
    print("Network Management Tool - Final Verification")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        test_module_imports,
        test_dependencies,
        test_nmap_functionality,
        test_cli_help
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All verification tests passed!")
        print("The Network Management Tool is ready for use.")
        return 0
    else:
        print("⚠️  Some verification tests failed.")
        print("Please check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())