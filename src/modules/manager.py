"""
Network Management Tool - Device Manager Module

This module provides device management capabilities including SSH access
and network interface control.
"""

import logging
import paramiko
import os
import socket
from .network_blocker import NetworkBlocker

class DeviceManager:
    """Device manager for accessing and managing network devices."""
    
    def __init__(self):
        """Initialize the device manager."""
        self.logger = logging.getLogger(__name__)
        # Cache for hostname resolutions to avoid repeated DNS lookups
        self._hostname_cache = {}
        # Initialize network blocker
        self.network_blocker = NetworkBlocker()
    
    def _resolve_hostname(self, ip_address):
        """
        Resolve hostname from IP address.
        
        Args:
            ip_address (str): The IP address to resolve.
            
        Returns:
            str: The hostname if resolved, otherwise the IP address.
        """
        # Check cache first
        if ip_address in self._hostname_cache:
            return self._hostname_cache[ip_address]
        
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            self.logger.info(f"Resolved hostname for {ip_address}: {hostname}")
            # Cache the result
            self._hostname_cache[ip_address] = hostname
            return hostname
        except Exception as e:
            self.logger.warning(f"Could not resolve hostname for {ip_address}: {e}")
            # Cache the IP as the result to avoid repeated failed lookups
            self._hostname_cache[ip_address] = ip_address
            return ip_address
    
    def _get_ssh_key_paths(self, ip_address, hostname=None, device_info=None):
        """
        Get potential SSH key paths based on IP, hostname, and device information.
        
        Args:
            ip_address (str): The target IP address.
            hostname (str): The target hostname from DNS resolution (optional).
            device_info (dict): Additional device information from fingerprinting (optional).
            
        Returns:
            list: List of potential SSH key paths ordered by priority.
        """
        # Expand user home directory
        home_dir = os.path.expanduser("~")
        
        # Build list of potential key paths
        key_paths = []
        added_paths = set()  # To avoid duplicates
        
        # Helper function to add paths safely
        def add_key_paths(*paths):
            for path in paths:
                if path not in added_paths and os.path.exists(path):
                    key_paths.append(path)
                    added_paths.add(path)
        
        # 1. Device-specific keys based on hostname from DNS resolution (high priority)
        if hostname and hostname != ip_address and hostname != 'Unknown':
            add_key_paths(
                os.path.join(home_dir, ".ssh", f"id_rsa_{hostname}"),
                os.path.join(home_dir, ".ssh", f"id_dsa_{hostname}"),
                os.path.join(home_dir, ".ssh", f"id_ecdsa_{hostname}"),
                os.path.join(home_dir, ".ssh", f"id_ed25519_{hostname}")
            )
        
        # 2. Keys based on device information from fingerprinting (highest priority if available)
        if device_info:
            # Add keys based on hostname from device info (highest priority)
            device_hostname = device_info.get('hostname')
            if device_hostname and device_hostname != 'Unknown' and device_hostname != ip_address:
                add_key_paths(
                    os.path.join(home_dir, ".ssh", f"id_rsa_{device_hostname}"),
                    os.path.join(home_dir, ".ssh", f"id_dsa_{device_hostname}"),
                    os.path.join(home_dir, ".ssh", f"id_ecdsa_{device_hostname}"),
                    os.path.join(home_dir, ".ssh", f"id_ed25519_{device_hostname}")
                )
            
            # Add keys based on OS type
            os_type = device_info.get('os', '').lower()
            if 'linux' in os_type or 'ubuntu' in os_type or 'centos' in os_type or 'debian' in os_type:
                add_key_paths(
                    os.path.join(home_dir, ".ssh", "id_rsa_linux"),
                    os.path.join(home_dir, ".ssh", "id_ed25519_linux")
                )
            elif 'windows' in os_type or 'windows server' in os_type:
                add_key_paths(
                    os.path.join(home_dir, ".ssh", "id_rsa_windows"),
                    os.path.join(home_dir, ".ssh", "id_ed25519_windows")
                )
            elif 'darwin' in os_type or 'macos' in os_type or 'mac os' in os_type:
                add_key_paths(
                    os.path.join(home_dir, ".ssh", "id_rsa_macos"),
                    os.path.join(home_dir, ".ssh", "id_ed25519_macos")
                )
        
        # 3. Device-specific keys based on IP address
        # Replace dots with underscores for IP-based key names
        ip_safe = ip_address.replace(".", "_")
        add_key_paths(
            os.path.join(home_dir, ".ssh", f"id_rsa_{ip_safe}"),
            os.path.join(home_dir, ".ssh", f"id_dsa_{ip_safe}"),
            os.path.join(home_dir, ".ssh", f"id_ecdsa_{ip_safe}"),
            os.path.join(home_dir, ".ssh", f"id_ed25519_{ip_safe}")
        )
        
        # 4. Standard SSH key locations (lowest priority)
        add_key_paths(
            os.path.join(home_dir, ".ssh", "id_rsa"),
            os.path.join(home_dir, ".ssh", "id_dsa"),
            os.path.join(home_dir, ".ssh", "id_ecdsa"),
            os.path.join(home_dir, ".ssh", "id_ed25519")
        )
        
        self.logger.info(f"Found {len(key_paths)} potential SSH keys for {ip_address}")
        if key_paths:
            self.logger.info(f"Potential keys: {key_paths}")
        return key_paths
    
    def _detect_ssh_key_for_device(self, ip_address, device_info=None):
        """
        Automatically detect SSH key for a device based on IP, hostname, and device information.
        
        Args:
            ip_address (str): The target IP address.
            device_info (dict): Additional device information from fingerprinting (optional).
            
        Returns:
            str: Path to SSH key if found, None otherwise.
        """
        # Resolve hostname
        hostname = self._resolve_hostname(ip_address)
        
        # Get potential key paths
        key_paths = self._get_ssh_key_paths(ip_address, hostname, device_info)
        
        # Return the first existing key
        for key_path in key_paths:
            if os.path.exists(key_path):
                self.logger.info(f"Found SSH key for {ip_address}: {key_path}")
                return key_path
        
        self.logger.warning(f"No SSH key found for {ip_address}")
        return None
    
    def manage_device(self, ip_address, username, password):
        """
        Manage a device by temporarily disabling its network interface.
        
        Args:
            ip_address (str): The IP address of the device to manage.
            username (str): The username for SSH access.
            password (str): The password for SSH access.
        """
        self.logger.info(f"Managing device: {ip_address}")
        
        try:
            # First, check if the device is reachable
            self.logger.info(f"Checking if device {ip_address} is reachable...")
            import socket
            import time
            
            # Try to ping the device first
            try:
                # Set a short timeout for the ping check
                socket.setdefaulttimeout(3)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip_address, 22))  # Check SSH port
                sock.close()
                
                if result != 0:
                    self.logger.warning(f"Device {ip_address} may not be reachable on SSH port 22")
                    print(f"Warning: Device {ip_address} may not be reachable on SSH port 22")
            except Exception as ping_error:
                self.logger.warning(f"Could not check reachability of {ip_address}: {ping_error}")
                print(f"Warning: Could not check reachability of {ip_address}")
            
            # Establish SSH connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.logger.info(f"Attempting to connect to {ip_address} with username {username}")
            ssh.connect(ip_address, username=username, password=password, timeout=10)
            
            # Command to disable network interface (example)
            # NOTE: This is a placeholder - actual implementation would need
            # to determine the correct interface and use appropriate commands
            command = "sudo ifconfig eth0 down"
            
            self.logger.info(f"Executing command: {command}")
            # Execute command with sudo password
            stdin, stdout, stderr = ssh.exec_command(f"echo {password} | sudo -S {command}", get_pty=True)
            
            # Check for errors
            error = stderr.read().decode()
            if error and "sorry, you must have a tty to run sudo" in error:
                self.logger.info("Trying alternative sudo method due to TTY requirement")
                # Try alternative method for sudo
                stdin, stdout, stderr = ssh.exec_command(command)
                stdin.write(password + '\n')
                stdin.flush()
                error = stderr.read().decode()
            
            if error and "password" in error.lower():
                self.logger.error(f"Authentication error managing device {ip_address}: {error}")
                print("Error: Authentication failed")
            elif error:
                self.logger.error(f"Error managing device {ip_address}: {error}")
                print(f"Error: {error}")
            else:
                output = stdout.read().decode()
                self.logger.info(f"Successfully managed device {ip_address}")
                print(f"Device {ip_address} network interface disabled successfully.")
            
            # Close connection
            ssh.close()
            
        except paramiko.AuthenticationException:
            self.logger.error(f"Authentication failed for device {ip_address}")
            print("Error: Authentication failed. Please check your credentials.")
        except paramiko.SSHException as e:
            self.logger.error(f"SSH error managing device {ip_address}: {e}")
            print(f"Error: SSH connection error: {e}")
        except socket.timeout:
            self.logger.error(f"Connection timeout when managing device {ip_address}")
            print("Error: Connection timeout. The device may not be reachable or SSH may not be enabled.")
        except socket.gaierror as e:
            self.logger.error(f"DNS resolution error for device {ip_address}: {e}")
            print(f"Error: Could not resolve hostname or IP address {ip_address}")
        except Exception as e:
            self.logger.error(f"Error managing device {ip_address}: {e}")
            print(f"Error managing device: {e}")
    
    def secure_manage_device(self, ip_address, ssh_key_path=None, username='admin', device_info=None):
        """
        Securely manage a device using SSH key authentication.
        
        Args:
            ip_address (str): The IP address of the device to manage.
            ssh_key_path (str): Path to the SSH private key file. If None, will auto-detect.
            username (str): The username for SSH access (default: 'admin').
            device_info (dict): Additional device information for key detection (optional).
        """
        self.logger.info(f"Securely managing device: {ip_address}")
        
        # Auto-detect SSH key if not provided
        if ssh_key_path is None:
            self.logger.info(f"Auto-detecting SSH key for {ip_address}")
            ssh_key_path = self._detect_ssh_key_for_device(ip_address, device_info)
            
            if ssh_key_path is None:
                self.logger.error(f"No SSH key found for device {ip_address}")
                print(f"Error: No SSH key found for device {ip_address}")
                print("Please provide a valid SSH key path or ensure keys exist in ~/.ssh/")
                print("Suggested key names:")
                print(f"  - ~/.ssh/id_rsa_{ip_address.replace('.', '_')}")
                if device_info:
                    hostname = device_info.get('hostname')
                    if hostname and hostname != 'Unknown' and hostname != ip_address:
                        print(f"  - ~/.ssh/id_rsa_{hostname}")
                    os_type = device_info.get('os', '').lower()
                    if 'linux' in os_type or 'ubuntu' in os_type or 'centos' in os_type:
                        print("  - ~/.ssh/id_rsa_linux")
                    elif 'windows' in os_type:
                        print("  - ~/.ssh/id_rsa_windows")
                print("  - ~/.ssh/id_rsa")
                return
        
        # Check if key file exists
        if not os.path.exists(ssh_key_path):
            self.logger.error(f"SSH key file not found: {ssh_key_path}")
            print(f"Error: SSH key file not found: {ssh_key_path}")
            return
        
        try:
            # First, check if the device is reachable
            self.logger.info(f"Checking if device {ip_address} is reachable...")
            import socket
            
            # Try to ping the device first
            try:
                # Set a short timeout for the ping check
                socket.setdefaulttimeout(3)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip_address, 22))  # Check SSH port
                sock.close()
                
                if result != 0:
                    self.logger.warning(f"Device {ip_address} may not be reachable on SSH port 22")
                    print(f"Warning: Device {ip_address} may not be reachable on SSH port 22")
            except Exception as ping_error:
                self.logger.warning(f"Could not check reachability of {ip_address}: {ping_error}")
                print(f"Warning: Could not check reachability of {ip_address}")
            
            # Establish SSH connection with key authentication
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Load private key
            self.logger.info(f"Loading private key from {ssh_key_path}")
            private_key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
            
            # Connect using key authentication
            self.logger.info(f"Attempting to connect to {ip_address} with username {username} using key authentication")
            ssh.connect(ip_address, username=username, pkey=private_key, timeout=10)
            
            # Command to disable network interface
            command = "sudo ifconfig eth0 down"
            
            self.logger.info(f"Executing command: {command}")
            # Execute command
            stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
            
            # Check for errors
            error = stderr.read().decode()
            if error:
                self.logger.error(f"Error managing device {ip_address}: {error}")
                print(f"Error: {error}")
            else:
                output = stdout.read().decode()
                self.logger.info(f"Successfully managed device {ip_address}")
                print(f"Device {ip_address} network interface disabled successfully.")
            
            # Close connection
            ssh.close()
            
        except paramiko.AuthenticationException:
            self.logger.error(f"Key authentication failed for device {ip_address}")
            print("Error: Key authentication failed.")
        except paramiko.ssh_exception.PasswordRequiredException:
            self.logger.error(f"SSH key requires password for device {ip_address}")
            print("Error: SSH key requires password. Please use password authentication instead.")
        except paramiko.SSHException as e:
            self.logger.error(f"SSH error managing device {ip_address}: {e}")
            print(f"Error: SSH connection error: {e}")
        except socket.timeout:
            self.logger.error(f"Connection timeout when managing device {ip_address}")
            print("Error: Connection timeout. The device may not be reachable or SSH may not be enabled.")
        except socket.gaierror as e:
            self.logger.error(f"DNS resolution error for device {ip_address}: {e}")
            print(f"Error: Could not resolve hostname or IP address {ip_address}")
        except Exception as e:
            self.logger.error(f"Error managing device {ip_address}: {e}")
            print(f"Error managing device: {e}")
    
    def test_connection(self, ip_address, username, password=None, ssh_key_path=None):
        """
        Test SSH connection to a device.
        
        Args:
            ip_address (str): The IP address of the device to test.
            username (str): The username for SSH access.
            password (str): The password for SSH access (optional).
            ssh_key_path (str): Path to the SSH private key file (optional).
            
        Returns:
            bool: True if connection successful, False otherwise.
        """
        self.logger.info(f"Testing connection to device: {ip_address}")
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if ssh_key_path and os.path.exists(ssh_key_path):
                # Use key authentication
                private_key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
                ssh.connect(ip_address, username=username, pkey=private_key, timeout=5)
            elif password:
                # Use password authentication
                ssh.connect(ip_address, username=username, password=password, timeout=5)
            else:
                self.logger.error("No authentication method provided")
                return False
            
            # Run a simple command to test connection
            stdin, stdout, stderr = ssh.exec_command("echo 'Connection test successful'")
            output = stdout.read().decode().strip()
            
            ssh.close()
            
            if "Connection test successful" in output:
                self.logger.info(f"Connection test successful for {ip_address}")
                return True
            else:
                self.logger.error(f"Connection test failed for {ip_address}")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection test failed for {ip_address}: {e}")
            return False

    def is_device_reachable(self, ip_address, port=22, timeout=5):
        """
        Check if a device is reachable on a specific port.
        
        Args:
            ip_address (str): The IP address of the device to check.
            port (int): The port to check (default: 22 for SSH).
            timeout (int): Connection timeout in seconds.
            
        Returns:
            bool: True if device is reachable, False otherwise.
        """
        self.logger.info(f"Checking if device {ip_address} is reachable on port {port}")
        
        try:
            import socket
            
            # Set timeout
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Try to connect
            result = sock.connect_ex((ip_address, port))
            sock.close()
            
            if result == 0:
                self.logger.info(f"Device {ip_address} is reachable on port {port}")
                return True
            else:
                self.logger.warning(f"Device {ip_address} is not reachable on port {port}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking reachability of {ip_address}: {e}")
            return False

    def block_device_network_access(self, ip_address, network_gateway="192.168.1.1"):
        """
        Block a device's network access by adding it to a firewall block list.
        
        Args:
            ip_address (str): The IP address of the device to block.
            network_gateway (str): The network gateway IP address.
            
        Returns:
            bool: True if blocking was successful, False otherwise.
        """
        self.logger.info(f"Blocking network access for device {ip_address}")
        
        try:
            # Even if device is not reachable, we should still block it to prevent future access
            # Check if device is reachable (for informational purposes only)
            if not self.is_device_reachable(ip_address, port=22, timeout=3):
                self.logger.info(f"Device {ip_address} is not reachable, but will still be blocked")
                print(f"Device {ip_address} is not reachable, but will still be blocked to prevent future access")
            
            # Use the NetworkBlocker to block the IP
            success = self.network_blocker.block_ip(ip_address)
            
            if success:
                self.logger.info(f"Successfully blocked device {ip_address} from accessing the network.")
                print(f"Successfully blocked device {ip_address} from accessing the network.")
                return True
            else:
                self.logger.error(f"Failed to block device {ip_address}")
                print(f"Failed to block device {ip_address}. This may be due to insufficient privileges. "
                      "Please run as administrator/root for full functionality.")
                return False
                
        except Exception as e:
            self.logger.error(f"Error blocking device {ip_address}: {e}")
            print(f"Error blocking device {ip_address}: {e}")
            return False

    def unblock_device_network_access(self, ip_address, network_gateway="192.168.1.1"):
        """
        Unblock a device's network access by removing it from a firewall block list.
        
        Args:
            ip_address (str): The IP address of the device to unblock.
            network_gateway (str): The network gateway IP address.
            
        Returns:
            bool: True if unblocking was successful, False otherwise.
        """
        self.logger.info(f"Unblocking network access for device {ip_address}")
        
        try:
            # Even if device is not reachable, we should still unblock it to restore future access
            # Check if device is reachable (for informational purposes only)
            if not self.is_device_reachable(ip_address, port=22, timeout=3):
                self.logger.info(f"Device {ip_address} is not reachable, but will still be unblocked")
                print(f"Device {ip_address} is not reachable, but will still be unblocked to restore future access")
            
            # Use the NetworkBlocker to unblock the IP
            success = self.network_blocker.unblock_ip(ip_address)
            
            if success:
                self.logger.info(f"Successfully unblocked device {ip_address} and restored network access.")
                print(f"Successfully unblocked device {ip_address} and restored network access.")
                return True
            else:
                self.logger.error(f"Failed to unblock device {ip_address}")
                print(f"Failed to unblock device {ip_address}. This may be due to insufficient privileges. "
                      "Please run as administrator/root for full functionality.")
                return False
                
        except Exception as e:
            self.logger.error(f"Error unblocking device {ip_address}: {e}")
            print(f"Error unblocking device {ip_address}: {e}")
            return False

if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.DEBUG)

    dm = DeviceManager()

    # Example usage
    ip = "192.168.1.1"
    username = "admin"
    password = "password"
    ssh_key_path = None  # Path to SSH key if you want to use key authentication

    # Test SSH connection
    if dm.test_connection(ip, username, password, ssh_key_path):
        print("SSH connection test passed!")
    else:
        print("SSH connection test failed.")

    # Manage device (temporarily disable network interface)
    dm.manage_device(ip, username, password)

    # Securely manage device using SSH key authentication
    dm.secure_manage_device(ip, ssh_key_path, username)

    # Backup device configuration
    backup_file = dm.backup_device_configuration(ip, username, ssh_key_path)
    if backup_file:
        print(f"Backup saved to: {backup_file}")
    else:
        print("Backup failed.")

    # Restore device configuration from backup file
    if dm.restore_device_configuration(ip, username, backup_file, ssh_key_path):
        print("Configuration restored successfully.")
    else:
        print("Configuration restore failed.")
