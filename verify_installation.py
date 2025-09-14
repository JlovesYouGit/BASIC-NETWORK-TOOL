#!/usr/bin/env python3
"""
Verification script for the Network Management Tool installation
"""

import sys
import os

def check_python_version():
    """Check if Python version is sufficient"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Version 3.6+ required")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        'scapy',
        'paramiko', 
        'nmap',
        'rich'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_nmap():
    """Check if Nmap is accessible"""
    print("\nChecking Nmap installation...")
    
    # Check if Nmap is in PATH
    import subprocess
    try:
        result = subprocess.run(['nmap', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ Nmap - Found ({version_line})")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check if Nmap is in break folder
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        break_folder = os.path.join(project_root, '..', 'break')
        nmap_path = os.path.join(break_folder, 'nmap.exe')
        
        if os.path.exists(nmap_path):
            import subprocess
            result = subprocess.run([nmap_path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ Nmap - Found in break folder ({version_line})")
                return True
    except Exception:
        pass
    
    print("❌ Nmap - Not found")
    print("Please install Nmap from https://nmap.org/download.html")
    print("Or run setup_nmap.bat to add it to PATH")
    return False

def check_modules():
    """Check if all modules can be imported"""
    print("\nChecking modules...")
    
    modules = [
        ('src.modules.scanner', 'NetworkScanner'),
        ('src.modules.manager', 'DeviceManager'),
        ('src.modules.dashboard', 'InteractiveDashboard')
    ]
    
    missing_modules = []
    
    for module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_path}.{class_name} - OK")
        except (ImportError, AttributeError) as e:
            print(f"❌ {module_path}.{class_name} - Error: {e}")
            missing_modules.append(module_path)
    
    return len(missing_modules) == 0

def main():
    print("Network Management Tool - Installation Verification")
    print("=" * 55)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_nmap,
        check_modules
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 55)
    if all(results):
        print("🎉 All checks passed! The tool is ready to use.")
        print("\nTry running: python run.py --help")
        return 0
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())