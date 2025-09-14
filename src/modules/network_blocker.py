"""
Network Blocking Module

This module provides functionality to block and unblock IP addresses from accessing the network
using actual system firewall commands with permanent rule persistence.
"""

import logging
import subprocess
import platform
import requests
import json
import os
import sys

class NetworkBlocker:
    """A class to handle network blocking operations using actual firewall commands with permanent persistence."""
    
    def __init__(self):
        """Initialize the network blocker."""
        self.logger = logging.getLogger(__name__)
        # Store blocked IPs in a file for persistence across reboots
        self.blocked_ips_file = os.path.join(os.path.dirname(__file__), "..", "..", "blocked_ips.json")
        self.blocked_ips = self._load_blocked_ips()
        self._check_privileges()
    
    def _check_privileges(self):
        """
        Check if the application has sufficient privileges to execute firewall commands.
        """
        try:
            if platform.system() == "Windows":
                # On Windows, check if we can execute netsh commands
                result = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], 
                                      capture_output=True, text=True)
                self.has_privileges = result.returncode == 0
            elif platform.system() == "Linux":
                # On Linux, check if we can execute iptables commands
                result = subprocess.run(["iptables", "-L"], capture_output=True, text=True)
                self.has_privileges = result.returncode == 0
            else:
                # On macOS, check if we can execute pfctl commands
                result = subprocess.run(["pfctl", "-sr"], capture_output=True, text=True)
                self.has_privileges = result.returncode == 0
                
            if not self.has_privileges:
                self.logger.warning("Insufficient privileges to execute firewall commands. "
                                  "Run as administrator/root for full functionality.")
                print("Warning: Insufficient privileges to execute firewall commands. "
                      "Run as administrator/root for full functionality.")
        except Exception as e:
            self.logger.warning(f"Error checking privileges: {e}")
            self.has_privileges = False
    
    def _load_blocked_ips(self):
        """
        Load blocked IPs from persistent storage.
        
        Returns:
            set: Set of blocked IP addresses.
        """
        try:
            if os.path.exists(self.blocked_ips_file):
                with open(self.blocked_ips_file, 'r') as f:
                    blocked_ips = set(json.load(f))
                    self.logger.info(f"Loaded {len(blocked_ips)} blocked IPs from persistent storage")
                    return blocked_ips
            else:
                self.logger.info("No existing blocked IPs file found")
                return set()
        except Exception as e:
            self.logger.error(f"Error loading blocked IPs: {e}")
            return set()
    
    def _save_blocked_ips(self):
        """
        Save blocked IPs to persistent storage.
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.blocked_ips_file), exist_ok=True)
            
            # Save blocked IPs to file
            with open(self.blocked_ips_file, 'w') as f:
                json.dump(list(self.blocked_ips), f)
            self.logger.info(f"Saved {len(self.blocked_ips)} blocked IPs to persistent storage")
        except Exception as e:
            self.logger.error(f"Error saving blocked IPs: {e}")
    
    def _execute_firewall_command(self, cmd, description):
        """
        Execute a firewall command and handle errors.
        
        Args:
            cmd (str or list): The command to execute.
            description (str): Description of the command for logging.
            
        Returns:
            bool: True if command was successful, False otherwise.
        """
        try:
            self.logger.info(f"Executing {description}: {cmd}")
            
            # Convert string command to list for better handling
            if isinstance(cmd, str):
                if platform.system() != "Windows":
                    cmd = cmd.split()
                else:
                    # On Windows, we need to use shell=True for netsh commands
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.logger.info(f"Successfully executed {description}")
                        return True
                    else:
                        self.logger.error(f"Failed to execute {description}. Error: {result.stderr}")
                        print(f"Error executing {description}: {result.stderr}")
                        return False
            
            # For non-Windows platforms or when cmd is already a list
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully executed {description}")
                return True
            else:
                self.logger.error(f"Failed to execute {description}. Error: {result.stderr}")
                print(f"Error executing {description}: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Exception while executing {description}: {e}")
            print(f"Exception while executing {description}: {e}")
            return False
    
    def _make_persistent_windows(self, ip_address):
        """
        Make blocking rules persistent on Windows.
        
        Args:
            ip_address (str): The IP address to block persistently.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Windows firewall rules are persistent by default
            # But we'll also create a startup script to ensure rules are re-added
            startup_script = os.path.join(os.path.dirname(__file__), "..", "..", "restore_blocked_ips.bat")
            
            # Create or append to startup script
            with open(startup_script, 'a') as f:
                f.write(f'netsh advfirewall firewall add rule name="Block {ip_address}" dir=in action=block remoteip={ip_address}\n')
                f.write(f'netsh advfirewall firewall add rule name="Block {ip_address} Out" dir=out action=block remoteip={ip_address}\n')
            
            self.logger.info(f"Added {ip_address} to Windows startup script")
            return True
        except Exception as e:
            self.logger.error(f"Error creating Windows startup script: {e}")
            return False
    
    def _make_persistent_linux(self, ip_address):
        """
        Make blocking rules persistent on Linux.
        
        Args:
            ip_address (str): The IP address to block persistently.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # For Linux, we'll save the rules to iptables-persistent or create a startup script
            # Check if iptables-persistent is available
            if self._execute_firewall_command(["which", "iptables-save"], "iptables-save check"):
                # Save current iptables rules
                self._execute_firewall_command(["iptables-save"], "iptables rules save")
                self.logger.info("Saved iptables rules to persistent storage")
            else:
                # Create a startup script
                startup_script = os.path.join(os.path.dirname(__file__), "..", "..", "restore_blocked_ips.sh")
                script_content = f"""#!/bin/bash
iptables -A INPUT -s {ip_address} -j DROP
iptables -A OUTPUT -d {ip_address} -j DROP
iptables -A FORWARD -s {ip_address} -j DROP
"""
                # Write script
                with open(startup_script, 'a') as f:
                    f.write(script_content)
                
                # Make script executable
                self._execute_firewall_command(["chmod", "+x", startup_script], "chmod startup script")
                
            return True
        except Exception as e:
            self.logger.error(f"Error creating Linux startup script: {e}")
            return False
    
    def _make_persistent_macos(self, ip_address):
        """
        Make blocking rules persistent on macOS.
        
        Args:
            ip_address (str): The IP address to block persistently.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # For macOS, we'll create a startup script
            startup_script = os.path.join(os.path.dirname(__file__), "..", "..", "restore_blocked_ips.sh")
            
            # Create or append to startup script
            with open(startup_script, 'a') as f:
                f.write(f"echo 'block in from {ip_address} to any' | pfctl -f -\n")
                f.write(f"echo 'block out from any to {ip_address}' | pfctl -f -\n")
            
            # Make script executable
            self._execute_firewall_command(["chmod", "+x", startup_script], "chmod macOS startup script")
            
            self.logger.info(f"Added {ip_address} to macOS startup script")
            return True
        except Exception as e:
            self.logger.error(f"Error creating macOS startup script: {e}")
            return False
    
    def block_ip(self, ip_address):
        """
        Block the specified IP address from accessing the network using system firewall with persistence.
        
        Args:
            ip_address (str): The IP address to block.
            
        Returns:
            bool: True if blocking was successful, False otherwise.
        """
        self.logger.info(f"Blocking IP address: {ip_address}")
        
        # Check if we have sufficient privileges
        if not self.has_privileges:
            self.logger.error("Insufficient privileges to block IP address. Run as administrator/root.")
            print("Error: Insufficient privileges to block IP address. Run as administrator/root.")
            return False
        
        try:
            # Store the blocked IP in memory and persistent storage
            self.blocked_ips.add(ip_address)
            self._save_blocked_ips()
            
            # Use system firewall commands to block the IP
            if platform.system() == "Windows":
                # Windows firewall command
                cmd = f'netsh advfirewall firewall add rule name="Block {ip_address}" dir=in action=block remoteip={ip_address}'
                success = self._execute_firewall_command(cmd, f"Windows firewall block rule for {ip_address}")
                
                if success:
                    # Also block outgoing connections
                    cmd = f'netsh advfirewall firewall add rule name="Block {ip_address} Out" dir=out action=block remoteip={ip_address}'
                    self._execute_firewall_command(cmd, f"Windows firewall outbound block rule for {ip_address}")
                    
                    # Make rules persistent
                    self._make_persistent_windows(ip_address)
                
                return success
                
            elif platform.system() == "Linux":
                # Linux iptables command for incoming traffic
                cmd = ["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]
                success = self._execute_firewall_command(cmd, f"Linux iptables INPUT rule for {ip_address}")
                
                if success:
                    # Also block outgoing traffic
                    cmd = ["iptables", "-A", "OUTPUT", "-d", ip_address, "-j", "DROP"]
                    self._execute_firewall_command(cmd, f"Linux iptables OUTPUT rule for {ip_address}")
                    
                    # Also block forwarding (if this is a router/gateway)
                    cmd = ["iptables", "-A", "FORWARD", "-s", ip_address, "-j", "DROP"]
                    self._execute_firewall_command(cmd, f"Linux iptables FORWARD rule for {ip_address}")
                    
                    # Make rules persistent
                    self._make_persistent_linux(ip_address)
                
                return success
                
            else:
                # macOS or other Unix-like systems (using pf - packet filter)
                cmd = ["pfctl", "-f", "-"]
                # Prepare the rule content
                rule_content = f"block in from {ip_address} to any\nblock out from any to {ip_address}\n"
                
                self.logger.info(f"Executing macOS pf block rule for {ip_address}")
                try:
                    result = subprocess.run(cmd, input=rule_content, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.logger.info(f"Successfully executed macOS pf block rule for {ip_address}")
                        success = True
                    else:
                        self.logger.error(f"Failed to execute macOS pf block rule for {ip_address}. Error: {result.stderr}")
                        print(f"Error executing macOS pf block rule for {ip_address}: {result.stderr}")
                        success = False
                        
                    if success:
                        # Make rules persistent
                        self._make_persistent_macos(ip_address)
                    
                    return success
                except Exception as e:
                    self.logger.error(f"Exception while executing macOS pf block rule for {ip_address}: {e}")
                    print(f"Exception while executing macOS pf block rule for {ip_address}: {e}")
                    return False
            
        except Exception as e:
            self.logger.error(f"Error blocking IP address {ip_address}: {e}")
            print(f"Error blocking IP address {ip_address}: {e}")
            return False
    
    def unblock_ip(self, ip_address):
        """
        Unblock the specified IP address to restore network access with persistence update.
        
        Args:
            ip_address (str): The IP address to unblock.
            
        Returns:
            bool: True if unblocking was successful, False otherwise.
        """
        self.logger.info(f"Unblocking IP address: {ip_address}")
        
        # Check if we have sufficient privileges
        if not self.has_privileges:
            self.logger.error("Insufficient privileges to unblock IP address. Run as administrator/root.")
            print("Error: Insufficient privileges to unblock IP address. Run as administrator/root.")
            return False
        
        try:
            # Remove the blocked IP from memory and persistent storage
            self.blocked_ips.discard(ip_address)
            self._save_blocked_ips()
            
            # Use system firewall commands to unblock the IP
            if platform.system() == "Windows":
                # Windows firewall command to delete inbound rule
                cmd = f'netsh advfirewall firewall delete rule name="Block {ip_address}"'
                success = self._execute_firewall_command(cmd, f"Windows firewall delete inbound rule for {ip_address}")
                
                if success:
                    # Also delete outbound rule
                    cmd = f'netsh advfirewall firewall delete rule name="Block {ip_address} Out"'
                    self._execute_firewall_command(cmd, f"Windows firewall delete outbound rule for {ip_address}")
                
                return success
                
            elif platform.system() == "Linux":
                # Linux iptables command to remove INPUT rule (try several variations)
                rules_to_try = [
                    ["iptables", "-D", "INPUT", "-s", ip_address, "-j", "DROP"],
                    ["iptables", "-D", "OUTPUT", "-d", ip_address, "-j", "DROP"],
                    ["iptables", "-D", "FORWARD", "-s", ip_address, "-j", "DROP"]
                ]
                
                success = True
                for cmd in rules_to_try:
                    rule_desc = f"Linux iptables delete rule: {' '.join(cmd)}"
                    if not self._execute_firewall_command(cmd, rule_desc):
                        # Log error but continue with other rules
                        self.logger.warning(f"Failed to execute: {rule_desc}")
                        success = False  # Mark as partial failure
                
                return success
                
            else:
                # macOS or other Unix-like systems
                # For macOS, we'll add pass rules to allow traffic
                cmd = ["pfctl", "-f", "-"]
                # Prepare the rule content
                rule_content = f"pass in from {ip_address} to any\npass out from any to {ip_address}\n"
                
                self.logger.info(f"Executing macOS pf pass rule for {ip_address}")
                try:
                    result = subprocess.run(cmd, input=rule_content, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.logger.info(f"Successfully executed macOS pf pass rule for {ip_address}")
                        return True
                    else:
                        self.logger.error(f"Failed to execute macOS pf pass rule for {ip_address}. Error: {result.stderr}")
                        print(f"Error executing macOS pf pass rule for {ip_address}: {result.stderr}")
                        return False
                except Exception as e:
                    self.logger.error(f"Exception while executing macOS pf pass rule for {ip_address}: {e}")
                    print(f"Exception while executing macOS pf pass rule for {ip_address}: {e}")
                    return False
            
        except Exception as e:
            self.logger.error(f"Error unblocking IP address {ip_address}: {e}")
            print(f"Error unblocking IP address {ip_address}: {e}")
            return False
    
    def restore_blocked_ips(self):
        """
        Restore all blocked IPs from persistent storage.
        
        Returns:
            bool: True if restoration was successful, False otherwise.
        """
        self.logger.info("Restoring blocked IPs from persistent storage")
        
        # Check if we have sufficient privileges
        if not self.has_privileges:
            self.logger.error("Insufficient privileges to restore blocked IPs. Run as administrator/root.")
            print("Error: Insufficient privileges to restore blocked IPs. Run as administrator/root.")
            return False
        
        try:
            success_count = 0
            for ip in self.blocked_ips:
                if self.block_ip(ip):
                    success_count += 1
                    self.logger.info(f"Restored block for IP: {ip}")
                else:
                    self.logger.error(f"Failed to restore block for IP: {ip}")
            
            self.logger.info(f"Restored {success_count}/{len(self.blocked_ips)} blocked IPs")
            return success_count == len(self.blocked_ips)
        except Exception as e:
            self.logger.error(f"Error restoring blocked IPs: {e}")
            return False
    
    def is_ip_blocked(self, ip_address):
        """
        Check if an IP address is currently blocked.
        
        Args:
            ip_address (str): The IP address to check.
            
        Returns:
            bool: True if the IP is blocked, False otherwise.
        """
        return ip_address in self.blocked_ips

# Example usage
if __name__ == "__main__":
    # Create a network blocker instance
    blocker = NetworkBlocker()
    
    # Restore any previously blocked IPs
    blocker.restore_blocked_ips()
    
    # Example detection logic (replace with your actual detection logic)
    detected_ip = blocker.detect_ip_address()  # This function should return the detected IP address
    
    if detected_ip:
        # Block the detected IP address
        success = blocker.block_ip(detected_ip)
        if success:
            print(f"Successfully blocked IP: {detected_ip}")
        else:
            print(f"Failed to block IP: {detected_ip}")
        
        # Check if IP is blocked
        if blocker.is_ip_blocked(detected_ip):
            print(f"IP {detected_ip} is currently blocked")
        
        # Unblock the IP address
        success = blocker.unblock_ip(detected_ip)
        if success:
            print(f"Successfully unblocked IP: {detected_ip}")
        else:
            print(f"Failed to unblock IP: {detected_ip}")