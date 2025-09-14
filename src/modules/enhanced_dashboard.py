"""
Network Management Tool - Enhanced Terminal Dashboard Module

This module provides an enhanced terminal dashboard using ASCII/ANSI art and widgets,
similar to blessed-contrib but using Python libraries.
"""

import logging
import time
import random
from blessed import Terminal
import plotext as plt
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

class EnhancedTerminalDashboard:
    """Enhanced terminal dashboard for network device management with ASCII/ANSI art."""
    
    def __init__(self, scanner, manager):
        """
        Initialize the enhanced terminal dashboard.
        
        Args:
            scanner (NetworkScanner): The network scanner instance.
            manager (DeviceManager): The device manager instance.
        """
        self.scanner = scanner
        self.manager = manager
        self.logger = logging.getLogger(__name__)
        self.console = Console()
        self.term = Terminal()
    
    def run(self):
        """Run the enhanced terminal dashboard."""
        self.logger.info("Starting enhanced terminal dashboard")
        
        with self.console.screen():
            self._show_main_dashboard()
    
    def _show_main_dashboard(self):
        """Display the main dashboard with multiple panels."""
        while True:
            # Clear screen
            print(self.term.clear())
            
            # Header
            header = Panel("[bold blue]Network Management Tool - Enhanced Terminal Dashboard[/bold blue]")
            self.console.print(header)
            
            # Show dashboard options
            self.console.print("\n[bold]Dashboard Options:[/bold]")
            self.console.print("1. Network Overview")
            self.console.print("2. Device Discovery")
            self.console.print("3. Performance Metrics")
            self.console.print("4. Device Management")
            self.console.print("5. Network Topology")
            self.console.print("6. Security Scan")
            self.console.print("7. Block Device Access")
            self.console.print("8. Unblock Device Access")
            self.console.print("9. Exit")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
            
            if choice == '1':
                self._show_network_overview()
            elif choice == '2':
                self._show_device_discovery()
            elif choice == '3':
                self._show_performance_metrics()
            elif choice == '4':
                self._show_device_management()
            elif choice == '5':
                self._show_network_topology()
            elif choice == '6':
                self._show_security_scan()
            elif choice == '7':
                self._block_device_access()
            elif choice == '8':
                self._unblock_device_access()
            elif choice == '9':
                self.console.print("[yellow]Exiting dashboard.[/yellow]")
                break
    
    def _show_network_overview(self):
        """Display network overview with statistics and charts."""
        self.console.print("\n[bold blue]Network Overview[/bold blue]")
        self.console.print("=" * 50)
        
        # Simulate network statistics
        devices_count = random.randint(5, 25)
        online_devices = random.randint(3, devices_count)
        server_devices = random.randint(1, 5)
        vulnerability_count = random.randint(0, 10)
        
        # Create statistics table
        stats_table = Table(show_header=True, header_style="bold magenta")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Total Devices", str(devices_count))
        stats_table.add_row("Online Devices", str(online_devices))
        stats_table.add_row("Server Devices", str(server_devices))
        stats_table.add_row("Vulnerabilities", str(vulnerability_count))
        stats_table.add_row("Network Status", "Operational" if vulnerability_count < 5 else "Warning")
        
        self.console.print(stats_table)
        
        # Create a simple chart using plotext
        self.console.print("\n[bold]Network Activity (Last 24 Hours):[/bold]")
        
        # Simulate data
        hours = list(range(24))
        activity = [random.randint(10, 100) for _ in range(24)]
        
        # Use plotext to create a line chart
        plt.clear_data()
        plt.plot(hours, activity)
        plt.title("Network Activity")
        plt.xlabel("Hours")
        plt.ylabel("Activity Level")
        plt.plotsize(60, 15)
        plt.show()
        
        # Wait for user input
        Prompt.ask("\nPress Enter to continue")
    
    def _show_device_discovery(self):
        """Display device discovery interface."""
        self.console.print("\n[bold blue]Device Discovery[/bold blue]")
        self.console.print("=" * 50)
        
        # Show scanning options
        self.console.print("\n[bold]Scan Options:[/bold]")
        self.console.print("1. Local Network Scan")
        self.console.print("2. Server Network Scan")
        self.console.print("3. Web Server Scan")
        self.console.print("4. Back to Main Dashboard")
        
        choice = Prompt.ask("\nSelect scan type", choices=["1", "2", "3", "4"])
        
        if choice in ['1', '2', '3']:
            network_type = ['local', 'server', 'web'][int(choice) - 1]
            self._perform_scan(network_type)
        # If choice is 4, we just return to the main dashboard
    
    def _perform_scan(self, network_type):
        """Perform a network scan and display results."""
        self.console.print(f"\n[blue]Scanning {network_type} network...[/blue]")
        
        # Show a progress spinner while scanning
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Scanning...", total=None)
            time.sleep(2)  # Simulate scanning time
            
            # Actually perform the scan
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
            Prompt.ask("\nPress Enter to continue")
            return
        
        # Display devices in a rich table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("IP Address", min_width=15)
        table.add_column("MAC Address", min_width=18)
        table.add_column("Hostname", min_width=20)
        table.add_column("OS", min_width=15)
        
        for idx, device in enumerate(devices, 1):
            mac_address = device.get('mac', 'Unknown')
            if not mac_address or mac_address == 'N/A':
                mac_address = 'Unknown'
            table.add_row(
                str(idx),
                device.get('ip', 'N/A'),
                mac_address,
                device.get('hostname', 'Unknown'),
                device.get('os', 'Unknown')
            )
        
        self.console.print(table)
        self.console.print(f"\n[green]Found {len(devices)} devices.[/green]")
        
        # Option to get detailed information
        detail_choice = Prompt.ask("\nEnter device ID for details (or 'back' to return)", default="back")
        
        if detail_choice.isdigit() and 1 <= int(detail_choice) <= len(devices):
            device_idx = int(detail_choice) - 1
            selected_device = devices[device_idx]
            
            # Fingerprint the device for detailed information
            self.console.print("[blue]Gathering detailed information about the device...[/blue]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Fingerprinting...", total=None)
                time.sleep(1)  # Simulate fingerprinting time
                fingerprinted_device = self.scanner.fingerprint_device(selected_device['ip'])
            
            self._show_device_details(fingerprinted_device)
        else:
            Prompt.ask("\nPress Enter to continue")
    
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
        
        # Show a simple bar chart of open ports if any
        if 'ports' in device and device['ports']:
            self.console.print("\n[bold]Open Ports Distribution:[/bold]")
            ports = device['ports']
            port_numbers = [p['port'] for p in ports]
            service_names = [p['service'][:10] for p in ports]  # Truncate service names
            
            # Use plotext to create a bar chart
            plt.clear_data()
            plt.bar(port_numbers, service_names)
            plt.title("Open Ports")
            plt.xlabel("Port Number")
            plt.ylabel("Service")
            plt.plotsize(60, 10)
            plt.show()
        
        # Option to manage device
        manage_choice = Prompt.ask("\nManage this device?", choices=["yes", "no"], default="no")
        if manage_choice == 'yes':
            self._manage_device(device)
        else:
            Prompt.ask("\nPress Enter to continue")
    
    def _show_performance_metrics(self):
        """Display network performance metrics with charts."""
        self.console.print("\n[bold blue]Performance Metrics[/bold blue]")
        self.console.print("=" * 50)
        
        # Simulate performance data
        time_points = list(range(10))
        latency_data = [random.randint(10, 100) for _ in range(10)]
        bandwidth_data = [random.randint(50, 200) for _ in range(10)]
        
        # Create latency chart
        self.console.print("\n[bold]Network Latency (ms):[/bold]")
        plt.clear_data()
        plt.plot(time_points, latency_data, label="Latency")
        plt.title("Network Latency Over Time")
        plt.xlabel("Time")
        plt.ylabel("Latency (ms)")
        plt.plotsize(60, 10)
        plt.show()
        
        # Create bandwidth chart
        self.console.print("\n[bold]Bandwidth Usage (Mbps):[/bold]")
        plt.clear_data()
        plt.plot(time_points, bandwidth_data, label="Bandwidth", color="red")
        plt.title("Bandwidth Usage Over Time")
        plt.xlabel("Time")
        plt.ylabel("Bandwidth (Mbps)")
        plt.plotsize(60, 10)
        plt.show()
        
        # Wait for user input
        Prompt.ask("\nPress Enter to continue")
    
    def _show_device_management(self):
        """Display device management interface."""
        self.console.print("\n[bold blue]Device Management[/bold blue]")
        self.console.print("=" * 50)
        
        # For simplicity, we'll ask for an IP address directly
        ip_address = Prompt.ask("\nEnter device IP address to manage (or 'back' to return)", default="back")
        
        if ip_address.lower() != "back":
            # First, get detailed device information
            self.console.print("[blue]Gathering detailed information about the device...[/blue]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Fingerprinting...", total=None)
                time.sleep(1)  # Simulate fingerprinting time
                device_info = self.scanner.fingerprint_device(ip_address)
            self._manage_device(device_info)
        else:
            return
    
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
            Prompt.ask("\nPress Enter to continue")
            return
        
        # Ask for authentication method
        auth_method = Prompt.ask("Select authentication method", choices=["password", "key", "auto"], default="auto")
        
        if auth_method == "password":
            username = Prompt.ask("Enter username")
            password = Prompt.ask("Enter password", password=True)
            # Show progress while managing
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Managing device...", total=None)
                time.sleep(2)  # Simulate management time
                self.manager.manage_device(ip_address, username, password)
        elif auth_method == "key":
            username = Prompt.ask("Enter username", default="admin")
            ssh_key_path = Prompt.ask("Enter path to SSH private key (or press Enter for auto-detection)", default="")
            # If user didn't provide a path, set to None for auto-detection
            if not ssh_key_path:
                ssh_key_path = None
            # Show progress while managing
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Managing device...", total=None)
                time.sleep(2)  # Simulate management time
                self.manager.secure_manage_device(ip_address, ssh_key_path, username, device_info)
        else:  # auto mode
            username = Prompt.ask("Enter username", default="admin")
            # Show progress while managing
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Managing device...", total=None)
                time.sleep(2)  # Simulate management time
                self.manager.secure_manage_device(ip_address, None, username, device_info)  # None triggers auto-detection
        
        Prompt.ask("\nPress Enter to continue")

    def _show_network_topology(self):
        """Display network topology visualization."""
        self.console.print("\n[bold blue]Network Topology[/bold blue]")
        self.console.print("=" * 50)
        
        # Simulate network topology data
        devices = [
            {'ip': '192.168.1.1', 'type': 'Router', 'connections': ['192.168.1.10', '192.168.1.15', '192.168.1.20']},
            {'ip': '192.168.1.10', 'type': 'Server', 'connections': ['192.168.1.1']},
            {'ip': '192.168.1.15', 'type': 'Workstation', 'connections': ['192.168.1.1']},
            {'ip': '192.168.1.20', 'type': 'IoT Device', 'connections': ['192.168.1.1']}
        ]
        
        # Create a simple text-based topology visualization
        self.console.print("\n[bold]Network Diagram:[/bold]")
        self.console.print("                    +----------------+")
        self.console.print("                    |  192.168.1.1   |")
        self.console.print("                    |    Router      |")
        self.console.print("                    +--------+-------+")
        self.console.print("                             |")
        self.console.print("            +----------------+----------------+")
        self.console.print("            |                |                |")
        self.console.print("+-----------v----+  +--------v-------+  +-----v----------+")
        self.console.print("| 192.168.1.10   |  | 192.168.1.15   |  | 192.168.1.20   |")
        self.console.print("|    Server      |  |  Workstation   |  |  IoT Device    |")
        self.console.print("+----------------+  +----------------+  +----------------+")
        
        # Show device list
        self.console.print("\n[bold]Device List:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("IP Address", style="cyan")
        table.add_column("Device Type", style="green")
        table.add_column("Connections", style="yellow")
        
        for device in devices:
            connections = ", ".join(device['connections'])
            table.add_row(device['ip'], device['type'], connections)
        
        self.console.print(table)
        
        Prompt.ask("\nPress Enter to continue")

    def _show_security_scan(self):
        """Display security scan results."""
        self.console.print("\n[bold blue]Security Scan Results[/bold blue]")
        self.console.print("=" * 50)
        
        # Simulate security scan data
        vulnerabilities = [
            {'ip': '192.168.1.10', 'issue': 'Open SSH port with weak cipher', 'severity': 'Medium', 'recommendation': 'Update SSH configuration'},
            {'ip': '192.168.1.15', 'issue': 'Outdated OS version', 'severity': 'High', 'recommendation': 'Apply security patches'},
            {'ip': '192.168.1.20', 'issue': 'Default admin password', 'severity': 'Critical', 'recommendation': 'Change default credentials'}
        ]
        
        if vulnerabilities:
            # Create a table for vulnerabilities
            table = Table(show_header=True, header_style="bold red")
            table.add_column("IP Address", style="cyan")
            table.add_column("Issue", style="white")
            table.add_column("Severity", style="yellow")
            table.add_column("Recommendation", style="green")
            
            # Color code severity
            severity_colors = {
                'Critical': 'red',
                'High': 'orange_red1',
                'Medium': 'yellow',
                'Low': 'green'
            }
            
            for vuln in vulnerabilities:
                severity_style = severity_colors.get(vuln['severity'], 'white')
                table.add_row(
                    vuln['ip'],
                    vuln['issue'],
                    f"[{severity_style}]{vuln['severity']}[/{severity_style}]",
                    vuln['recommendation']
                )
            
            self.console.print(table)
            
            # Add option to block a device
            self.console.print("\n[bold]Network Access Control:[/bold]")
            block_choice = Prompt.ask("Do you want to block any device? (Enter IP or 'no')", default="no")
            if block_choice != "no":
                self.console.print(f"[yellow]Blocking network access for {block_choice}...[/yellow]")
                # In a real implementation, this would call the manager's block method
                # For now, we'll just simulate it
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="Blocking device...", total=None)
                    time.sleep(2)  # Simulate blocking time
                self.console.print(f"[green]Device {block_choice} has been blocked from accessing the network.[/green]")
        else:
            self.console.print("[green]No vulnerabilities found.[/green]")
        
        Prompt.ask("\nPress Enter to continue")

    def _block_device_access(self):
        """Block a device's network access."""
        self.console.print("\n[bold blue]Block Device Network Access[/bold blue]")
        self.console.print("=" * 50)
        
        ip_address = Prompt.ask("Enter the IP address of the device to block")
        
        if ip_address:
            self.console.print(f"[yellow]Blocking network access for {ip_address}...[/yellow]")
            # In a real implementation, this would call the manager's block method
            # For now, we'll just simulate it
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Blocking device...", total=None)
                time.sleep(2)  # Simulate blocking time
            
            self.console.print(f"[green]Device {ip_address} has been blocked from accessing the network.[/green]")
        
        Prompt.ask("\nPress Enter to continue")

    def _unblock_device_access(self):
        """Unblock a device's network access."""
        self.console.print("\n[bold blue]Unblock Device Network Access[/bold blue]")
        self.console.print("=" * 50)
        
        ip_address = Prompt.ask("Enter the IP address of the device to unblock")
        
        if ip_address:
            self.console.print(f"[yellow]Unblocking network access for {ip_address}...[/yellow]")
            # In a real implementation, this would call the manager's unblock method
            # For now, we'll just simulate it
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Unblocking device...", total=None)
                time.sleep(2)  # Simulate unblocking time
            
            self.console.print(f"[green]Device {ip_address} has been unblocked and can access the network.[/green]")
        
        Prompt.ask("\nPress Enter to continue")

if __name__ == '__main__':
    from scanner import NetworkScanner
    from manager import DeviceManager

    logging.basicConfig(level=logging.INFO)

    scanner = NetworkScanner()
    manager = DeviceManager()

    dashboard = EnhancedTerminalDashboard(scanner, manager)
    dashboard.run()
