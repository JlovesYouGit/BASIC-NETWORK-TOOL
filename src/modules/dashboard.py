"""
Network Management Tool - Interactive Dashboard Module

This module provides an interactive dashboard for viewing and managing devices.
"""

import logging
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

class InteractiveDashboard:
    """Interactive dashboard for network device management."""
    
    def __init__(self, scanner, manager):
        """
        Initialize the interactive dashboard.
        
        Args:
            scanner (NetworkScanner): The network scanner instance.
            manager (DeviceManager): The device manager instance.
        """
        self.scanner = scanner
        self.manager = manager
        self.logger = logging.getLogger(__name__)
        self.console = Console()
    
    def run(self):
        """Run the interactive dashboard."""
        self.logger.info("Starting interactive dashboard")
        self.console.print("[bold blue]Network Management Tool - Interactive Dashboard[/bold blue]")
        self.console.print("=" * 50)
        
        while True:
            self.console.print("\n[bold]Options:[/bold]")
            self.console.print("1. Scan local network")
            self.console.print("2. Scan server network")
            self.console.print("3. Scan web server")
            self.console.print("4. Exit")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4"])
            
            if choice == '1':
                self._scan_and_display('local')
            elif choice == '2':
                self._scan_and_display('server')
            elif choice == '3':
                self._scan_and_display('web')
            elif choice == '4':
                self.console.print("[yellow]Exiting dashboard.[/yellow]")
                break
    
    def _scan_and_display(self, network_type):
        """
        Scan a network type and display results.
        
        Args:
            network_type (str): The type of network to scan.
        """
        self.console.print(f"\n[blue]Scanning {network_type} network...[/blue]")
        
        if network_type == 'local':
            devices = self.scanner.scan_local_network()
        elif network_type == 'server':
            devices = self.scanner.scan_server_network()
        elif network_type == 'web':
            devices = self.scanner.scan_web_server()
        else:
            self.console.print("[red]Invalid network type.[/red]")
            return
        
        if not devices:
            self.console.print("[yellow]No devices found.[/yellow]")
            return
        
        # Display devices in a rich table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("IP Address", min_width=15)
        table.add_column("MAC Address", min_width=18)
        
        for idx, device in enumerate(devices, 1):
            mac_address = device.get('mac', 'Unknown')
            if not mac_address or mac_address == 'N/A':
                mac_address = 'Unknown'
            table.add_row(str(idx), device['ip'], mac_address)
        
        self.console.print(table)
        self.console.print(f"\n[green]Found {len(devices)} devices.[/green]")
        
        # Option to get detailed information
        detail_choice = Prompt.ask("\nEnter device ID for details (or 'back' to return)", default="back")
        
        if detail_choice.isdigit() and 1 <= int(detail_choice) <= len(devices):
            device_idx = int(detail_choice) - 1
            selected_device = devices[device_idx]
            
            # Fingerprint the device for detailed information
            self.console.print("[blue]Gathering detailed information about the device...[/blue]")
            fingerprinted_device = self.scanner.fingerprint_device(selected_device['ip'])
            self._show_device_details(fingerprinted_device)
    
    def _show_device_details(self, device):
        """
        Show detailed information about a device.
        
        Args:
            device (dict): The device information.
        """
        self.console.print(f"\n[bold]Device Details for {device['ip']}:[/bold]")
        self.console.print("-" * 40)
        
        # Create a table for device details
        table = Table(show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        for key, value in device.items():
            if key == 'ports':
                # Handle ports specially
                if value:
                    ports_str = ", ".join([f"{p['port']} ({p['service']} {p['version']})" for p in value])
                    table.add_row(key.capitalize(), ports_str)
                else:
                    table.add_row(key.capitalize(), "No open ports detected")
            else:
                table.add_row(key.capitalize(), str(value))
        
        self.console.print(table)
        
        # Option to manage device
        manage_choice = Prompt.ask("\nManage this device?", choices=["yes", "no"], default="no")
        if manage_choice == 'yes':
            # First, get detailed device information
            self.console.print("[blue]Gathering detailed information about the device...[/blue]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Fingerprinting...", total=None)
                time.sleep(1)  # Simulate fingerprinting time
                device_info = self.scanner.fingerprint_device(device['ip'])
            self._manage_device(device_info)
    
    def _manage_device(self, device_info):
        """
        Manage a device by temporarily disabling its network interface.
        
        Args:
            device_info (dict): The device information.
        """
        ip_address = device_info['ip']
        self.console.print(f"\n[bold]Managing device {ip_address}[/bold]")
        
        # Check if device is reachable before attempting to manage it
        if not self.manager.is_device_reachable(ip_address):
            self.console.print(f"[red]Device {ip_address} is not reachable. Please check the IP address and network connectivity.[/red]")
            return
        
        # Ask for authentication method
        auth_method = Prompt.ask("Select authentication method", choices=["password", "key", "auto"], default="auto")
        
        if auth_method == "password":
            username = Prompt.ask("Enter username")
            password = Prompt.ask("Enter password", password=True)
            self.manager.manage_device(ip_address, username, password)
        elif auth_method == "key":
            username = Prompt.ask("Enter username", default="admin")
            ssh_key_path = Prompt.ask("Enter path to SSH private key (or press Enter for auto-detection)", default="")
            # If user didn't provide a path, set to None for auto-detection
            if not ssh_key_path:
                ssh_key_path = None
            self.manager.secure_manage_device(ip_address, ssh_key_path, username, device_info)
        else:  # auto mode
            username = Prompt.ask("Enter username", default="admin")
            self.manager.secure_manage_device(ip_address, None, username, device_info)  # None triggers auto-detection
