#!/usr/bin/env python3
"""
Network Management Tool - Main Application Entry Point

This tool provides comprehensive network scanning, device management,
and security monitoring capabilities.
"""

import argparse
import logging
import os
from modules.scanner import NetworkScanner
from modules.manager import DeviceManager
from modules.dashboard import InteractiveDashboard
from modules.enhanced_dashboard import EnhancedTerminalDashboard

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('network_tool.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(description='Network Device Manager')
    parser.add_argument('--scan', choices=['local', 'server', 'web'], 
                       help='Scan a network type')
    parser.add_argument('--manage', metavar='IP', help='Manage a device by IP address')
    parser.add_argument('--dashboard', action='store_true', 
                       help='Launch interactive dashboard')
    parser.add_argument('--enhanced-dashboard', action='store_true',
                       help='Launch enhanced terminal dashboard')
    parser.add_argument('--monitor-traffic', metavar='INTERFACE', 
                       help='Monitor network traffic on specified interface')
    parser.add_argument('--backup-config', nargs=2, metavar=('IP', 'USERNAME'),
                       help='Backup device configuration (IP USERNAME)')
    parser.add_argument('--restore-config', nargs=3, metavar=('IP', 'USERNAME', 'BACKUP_FILE'),
                       help='Restore device configuration (IP USERNAME BACKUP_FILE)')
    parser.add_argument('--block-device', metavar='IP', 
                       help='Block a device from accessing the network')
    parser.add_argument('--unblock-device', metavar='IP', 
                       help='Unblock a device and restore network access')
    
    args = parser.parse_args()
    
    scanner = NetworkScanner()
    manager = DeviceManager()
    
    if args.enhanced_dashboard:
        # Launch enhanced terminal dashboard
        enhanced_dashboard = EnhancedTerminalDashboard(scanner, manager)
        enhanced_dashboard.run()
    elif args.dashboard:
        # Launch interactive dashboard
        dashboard = InteractiveDashboard(scanner, manager)
        dashboard.run()
    elif args.block_device:
        # Block a device from network access
        ip_address = args.block_device
        print(f"Blocking network access for device {ip_address}...")
        # Even if device is not reachable, we should still block it
        # Check if device is reachable (for informational purposes only)
        if not manager.is_device_reachable(ip_address):
            print(f"Device {ip_address} is not reachable, but will still be blocked to prevent future access")
        success = manager.block_device_network_access(ip_address)
        if success:
            print(f"Device {ip_address} has been successfully blocked from accessing the network.")
        else:
            print(f"Failed to block device {ip_address}. Check logs for details.")
    elif args.unblock_device:
        # Unblock a device and restore network access
        ip_address = args.unblock_device
        print(f"Unblocking network access for device {ip_address}...")
        # Even if device is not reachable, we should still unblock it
        # Check if device is reachable (for informational purposes only)
        if not manager.is_device_reachable(ip_address):
            print(f"Device {ip_address} is not reachable, but will still be unblocked to restore future access")
        success = manager.unblock_device_network_access(ip_address)
        if success:
            print(f"Device {ip_address} has been successfully unblocked and can access the network.")
        else:
            print(f"Failed to unblock device {ip_address}. Check logs for details.")
    elif args.monitor_traffic:
        # Monitor network traffic
        interface = args.monitor_traffic
        print(f"Monitoring network traffic on interface {interface}...")
        traffic_stats = scanner.monitor_network_traffic(interface, duration=60)
        print("Traffic Statistics:")
        print(f"  Interface: {traffic_stats.get('interface', 'N/A')}")
        print(f"  Duration: {traffic_stats.get('duration', 0)} seconds")
        print(f"  Packets Captured: {traffic_stats.get('packets_captured', 0)}")
        print(f"  Bytes Transferred: {traffic_stats.get('bytes_transferred', 0)}")
        if 'protocols' in traffic_stats:
            print("  Protocol Distribution:")
            for protocol, count in traffic_stats['protocols'].items():
                print(f"    {protocol}: {count}")
    elif args.backup_config:
        # Backup device configuration
        ip_address, username = args.backup_config
        print(f"Backing up configuration for device {ip_address}...")
        # For security, we'll use key-based authentication only
        # In a real implementation, you would specify the key path
        backup_path = manager.backup_device_configuration(ip_address, username)
        if backup_path:
            print(f"Configuration backed up successfully to: {backup_path}")
        else:
            print("Failed to backup configuration.")
    elif args.restore_config:
        # Restore device configuration
        ip_address, username, backup_file = args.restore_config
        print(f"Restoring configuration for device {ip_address} from {backup_file}...")
        # For security, we'll use key-based authentication only
        # In a real implementation, you would specify the key path
        success = manager.restore_device_configuration(ip_address, username, backup_file)
        if success:
            print("Configuration restored successfully.")
        else:
            print("Failed to restore configuration.")
    elif args.scan:
        # Perform network scan based on type
        devices = []
        if args.scan == 'local':
            devices = scanner.scan_local_network()
        elif args.scan == 'server':
            devices = scanner.scan_server_network()
        elif args.scan == 'web':
            devices = scanner.scan_web_server()
        
        # Display discovered devices
        print("Discovered devices:")
        print("IP" + " "*18+"MAC")
        for device in devices:
            mac_address = device.get('mac', 'Unknown')
            if not mac_address or mac_address == 'N/A':
                mac_address = 'Unknown'
            print(f"{device['ip']:<20} {mac_address}")
    elif args.manage:
        # Manage a specific device
        ip_address = args.manage
        
        # First, get detailed device information
        print("Gathering detailed information about the device...")
        scanner = NetworkScanner()
        device_info = scanner.fingerprint_device(ip_address)
        
        # Ask for authentication method
        auth_method = input("Select authentication method (password/key/auto): ").lower()
        
        if auth_method == "key":
            username = input(f"Enter username for {ip_address}: ") or "admin"
            ssh_key_path = input(f"Enter path to SSH private key for {ip_address} (or press Enter for auto-detection): ") or None
            # Expand the path to handle ~ if provided
            if ssh_key_path:
                import os
                ssh_key_path = os.path.expanduser(ssh_key_path)
            
            print(f"You are about to manage device {ip_address}.")
            confirm = input("Do you want to temporarily disable its network interface? (yes/no): ")
            
            if confirm.lower() == 'yes':
                # Check if device is reachable before attempting to manage it
                if manager.is_device_reachable(ip_address):
                    manager.secure_manage_device(ip_address, ssh_key_path, username, device_info)
                else:
                    print(f"Device {ip_address} is not reachable. Please check the IP address and network connectivity.")
            else:
                print("Management cancelled.")
        elif auth_method == "auto":
            username = input(f"Enter username for {ip_address}: ") or "admin"
            
            print(f"You are about to manage device {ip_address}.")
            confirm = input("Do you want to temporarily disable its network interface? (yes/no): ")
            
            if confirm.lower() == 'yes':
                # Check if device is reachable before attempting to manage it
                if manager.is_device_reachable(ip_address):
                    manager.secure_manage_device(ip_address, None, username, device_info)  # None triggers auto-detection
                else:
                    print(f"Device {ip_address} is not reachable. Please check the IP address and network connectivity.")
            else:
                print("Management cancelled.")
        else:
            # Default to password authentication
            username = input(f"Enter username for {ip_address}: ")
            password = input(f"Enter password for {ip_address}: ")
            
            print(f"You are about to manage device {ip_address}.")
            confirm = input("Do you want to temporarily disable its network interface? (yes/no): ")
            
            if confirm.lower() == 'yes':
                # Check if device is reachable before attempting to manage it
                if manager.is_device_reachable(ip_address):
                    manager.manage_device(ip_address, username, password)
                else:
                    print(f"Device {ip_address} is not reachable. Please check the IP address and network connectivity.")
            else:
                print("Management cancelled.")
    else:
        # Show help if no arguments provided
        parser.print_help()

if __name__ == '__main__':
    main()