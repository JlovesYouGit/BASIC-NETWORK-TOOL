#!/usr/bin/env python3
"""
Script to restore blocked IPs on system startup
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.network_blocker import NetworkBlocker

def restore_blocked_ips_on_startup():
    """
    Restore all blocked IPs from persistent storage on system startup.
    """
    print("Restoring blocked IPs from persistent storage...")
    
    try:
        # Create a network blocker instance
        blocker = NetworkBlocker()
        
        # Restore all blocked IPs
        success = blocker.restore_blocked_ips()
        
        if success:
            print("Successfully restored all blocked IPs")
        else:
            print("Failed to restore some blocked IPs")
            
    except Exception as e:
        print(f"Error restoring blocked IPs: {e}")

if __name__ == "__main__":
    restore_blocked_ips_on_startup()