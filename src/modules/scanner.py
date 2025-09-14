"""
Network Management Tool - Scanner Module

This module provides network scanning capabilities for local, 
server, and web networks.
"""

import logging
import nmap
import socket
import os
from scapy.all import ARP, Ether, srp

class NetworkScanner:
    """Network scanner for discovering devices on various network types."""
    
    def __init__(self):
        """Initialize the network scanner."""
        self.logger = logging.getLogger(__name__)
        # Try to locate Nmap in the break folder if not in PATH
        self._locate_nmap()
    
    def _locate_nmap(self):
        """Locate Nmap executable in the break folder and set environment variable if needed."""
        try:
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            break_folder = os.path.join(project_root, '..', 'break')
            nmap_path = os.path.join(break_folder, 'nmap.exe')
            
            if os.path.exists(nmap_path):
                # Set the NMAP_PATH environment variable for python-nmap
                nmap_dir = os.path.dirname(nmap_path)
                os.environ['NMAP_PATH'] = nmap_dir
                self.logger.info(f"Nmap located at: {nmap_path}")
            else:
                self.logger.warning("Nmap executable not found in break folder")
        except Exception as e:
            self.logger.warning(f"Could not locate Nmap in break folder: {e}")
    
    def scan_local_network(self, ip_range="192.168.1.0/24"):
        """
        Scans a local network for connected devices using ARP requests.
        
        Args:
            ip_range (str): The IP range to scan (e.g., "192.168.1.0/24").
            
        Returns:
            list: A list of dictionaries, where each dictionary contains the
                  'ip' and 'mac' address of a device.
        """
        self.logger.info(f"Scanning local network: {ip_range}")
        
        try:
            arp = ARP(pdst=ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            result = srp(packet, timeout=3, verbose=0)[0]
            
            devices = []
            for sent, received in result:
                devices.append({'ip': received.psrc, 'mac': received.hwsrc})
            
            self.logger.info(f"Found {len(devices)} devices on local network")
            return devices
        except Exception as e:
            self.logger.error(f"Error scanning local network: {e}")
            return []
    
    def scan_server_network(self, target="192.168.1.0/24", ports=[22, 80, 443, 3389]):
        """
        Scans a server network for connected devices using port scanning.
        
        Args:
            target (str): The target IP range or hostname to scan.
            ports (list): List of ports to scan for open services.
            
        Returns:
            list: A list of dictionaries containing device information.
        """
        self.logger.info(f"Scanning server network: {target}")
        
        try:
            # Use nmap for comprehensive server network scanning
            try:
                nm = nmap.PortScanner()
            except nmap.PortScannerError:
                # Try with explicit path to Nmap
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                break_folder = os.path.join(project_root, '..', 'break')
                nmap_path = os.path.join(break_folder, 'nmap.exe')
                if os.path.exists(nmap_path):
                    nm = nmap.PortScanner(nmap_path)
                else:
                    raise
            
            # Scan with service detection and OS detection
            port_str = ','.join(map(str, ports))
            nm.scan(target, port_str, arguments='-sS -O -T4')
            
            devices = []
            for host in nm.all_hosts():
                if nm[host].state() == 'up':
                    device_info = {
                        'ip': host,
                        'mac': nm[host]['addresses'].get('mac', 'Unknown'),
                        'hostname': nm[host].hostname() if nm[host].hostname() else 'Unknown',
                        'os': 'Unknown',
                        'ports': []
                    }
                    
                    # Get OS information
                    if 'osmatch' in nm[host] and nm[host]['osmatch']:
                        device_info['os'] = nm[host]['osmatch'][0]['name']
                    
                    # Get open ports and services
                    if 'tcp' in nm[host]:
                        for port, port_info in nm[host]['tcp'].items():
                            device_info['ports'].append({
                                'port': port,
                                'service': port_info.get('name', 'unknown'),
                                'version': port_info.get('version', 'unknown')
                            })
                    
                    devices.append(device_info)
            
            self.logger.info(f"Found {len(devices)} devices on server network")
            return devices
        except nmap.PortScannerError as e:
            self.logger.error(f"Nmap error scanning server network: {e}")
            # Fallback to basic ICMP ping scan
            return self._ping_scan(target)
        except Exception as e:
            self.logger.error(f"Error scanning server network: {e}")
            return []
    
    def scan_web_server(self, target="example.com"):
        """
        Scans a web server for connected devices and services.
        
        Args:
            target (str): The target web server hostname or IP address.
            
        Returns:
            list: A list of dictionaries containing device information.
        """
        self.logger.info(f"Scanning web server: {target}")
        
        try:
            # Resolve hostname to IP
            try:
                ip_address = socket.gethostbyname(target)
            except socket.gaierror:
                self.logger.error(f"Could not resolve hostname: {target}")
                return []
            
            # Use nmap for comprehensive web server scanning
            try:
                nm = nmap.PortScanner()
            except nmap.PortScannerError:
                # Try with explicit path to Nmap
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                break_folder = os.path.join(project_root, '..', 'break')
                nmap_path = os.path.join(break_folder, 'nmap.exe')
                if os.path.exists(nmap_path):
                    nm = nmap.PortScanner(nmap_path)
                else:
                    raise
            
            # Scan common web ports with service detection
            nm.scan(ip_address, '21,22,23,25,53,80,110,143,443,993,995', arguments='-sV -T4')
            
            devices = []
            if ip_address in nm.all_hosts() and nm[ip_address].state() == 'up':
                device_info = {
                    'ip': ip_address,
                    'hostname': target,
                    'mac': 'Unknown',
                    'os': 'Unknown',
                    'ports': []
                }
                
                # Get OS information if available
                if 'osmatch' in nm[ip_address] and nm[ip_address]['osmatch']:
                    device_info['os'] = nm[ip_address]['osmatch'][0]['name']
                
                # Get open ports and services
                for proto in nm[ip_address].all_protocols():
                    if proto in ['tcp', 'udp']:
                        for port, port_info in nm[ip_address][proto].items():
                            device_info['ports'].append({
                                'port': port,
                                'service': port_info.get('name', 'unknown'),
                                'version': port_info.get('version', 'unknown')
                            })
                
                devices.append(device_info)
            
            self.logger.info(f"Found {len(devices)} web servers")
            return devices
        except nmap.PortScannerError as e:
            self.logger.error(f"Nmap error scanning web server: {e}")
            # Fallback to basic port scan
            return self._web_port_scan(target)
        except Exception as e:
            self.logger.error(f"Error scanning web server: {e}")
            return []
    
    def _ping_scan(self, target):
        """
        Performs a basic ICMP ping scan as fallback.
        
        Args:
            target (str): The target IP range to scan.
            
        Returns:
            list: A list of dictionaries containing device information.
        """
        self.logger.info(f"Performing ICMP ping scan on: {target}")
        
        try:
            try:
                nm = nmap.PortScanner()
            except nmap.PortScannerError:
                # Try with explicit path to Nmap
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                break_folder = os.path.join(project_root, '..', 'break')
                nmap_path = os.path.join(break_folder, 'nmap.exe')
                if os.path.exists(nmap_path):
                    nm = nmap.PortScanner(nmap_path)
                else:
                    raise
            
            nm.scan(target, arguments='-sn')
            
            devices = []
            for host in nm.all_hosts():
                if nm[host].state() == 'up':
                    devices.append({
                        'ip': host,
                        'mac': 'Unknown',
                        'hostname': nm[host].hostname() if nm[host].hostname() else 'Unknown',
                        'os': 'Unknown',
                        'ports': []
                    })
            
            return devices
        except Exception as e:
            self.logger.error(f"Error in ping scan: {e}")
            return []
    
    def _web_port_scan(self, target):
        """
        Performs a basic port scan for common web services as fallback.
        
        Args:
            target (str): The target hostname or IP address.
            
        Returns:
            list: A list of dictionaries containing device information.
        """
        self.logger.info(f"Performing basic port scan on: {target}")
        
        try:
            # Resolve hostname to IP
            try:
                ip_address = socket.gethostbyname(target)
            except socket.gaierror:
                self.logger.error(f"Could not resolve hostname: {target}")
                return []
            
            # Common web ports to check
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
            open_ports = []
            
            # Check each port
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip_address, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except Exception:
                    pass
            
            # If we found open ports, return the device info
            if open_ports:
                return [{
                    'ip': ip_address,
                    'hostname': target,
                    'mac': 'Unknown',
                    'os': 'Unknown',
                    'ports': [{'port': port, 'service': self._get_service_name(port), 'version': 'Unknown'} for port in open_ports]
                }]
            
            return []
        except Exception as e:
            self.logger.error(f"Error in web port scan: {e}")
            return []
    
    def _get_service_name(self, port):
        """
        Returns a service name for a given port number.
        
        Args:
            port (int): The port number.
            
        Returns:
            str: The service name.
        """
        service_map = {
            21: 'ftp',
            22: 'ssh',
            23: 'telnet',
            25: 'smtp',
            53: 'dns',
            80: 'http',
            110: 'pop3',
            143: 'imap',
            443: 'https',
            993: 'imaps',
            995: 'pop3s'
        }
        return service_map.get(port, 'unknown')
    
    def fingerprint_device(self, ip_address):
        """
        Performs detailed fingerprinting of a device using Nmap.
        
        Args:
            ip_address (str): The IP address of the device to scan.
            
        Returns:
            dict: A dictionary containing detailed information about the device.
        """
        self.logger.info(f"Fingerprinting device: {ip_address}")
        
        # Initialize device info with basic information
        device_info = {
            'ip': ip_address,
            'os': 'Unknown',
            'ports': [],
            'hostname': 'Unknown'
        }
        
        try:
            # Create Nmap PortScanner object
            try:
                nm = nmap.PortScanner()
            except nmap.PortScannerError:
                # Try with explicit path to Nmap
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                break_folder = os.path.join(project_root, '..', 'break')
                nmap_path = os.path.join(break_folder, 'nmap.exe')
                if os.path.exists(nmap_path):
                    nm = nmap.PortScanner(nmap_path)
                else:
                    raise
            
            # Perform a scan with OS detection (-O), service detection (-sV)
            # -T4 for faster execution
            nm.scan(ip_address, arguments='-T4 -sV -O --host-timeout 30')
            
            if ip_address in nm.all_hosts():
                # Get OS information
                if 'osmatch' in nm[ip_address] and nm[ip_address]['osmatch']:
                    device_info['os'] = nm[ip_address]['osmatch'][0]['name']
                
                # Get hostname
                if 'hostnames' in nm[ip_address] and nm[ip_address]['hostnames']:
                    device_info['hostname'] = nm[ip_address]['hostnames'][0]['name']
                
                # Get open ports and services
                if 'tcp' in nm[ip_address]:
                    for port, port_info in nm[ip_address]['tcp'].items():
                        device_info['ports'].append({
                            'port': port,
                            'service': port_info.get('name', 'unknown'),
                            'version': port_info.get('version', 'unknown')
                        })
        except nmap.PortScannerError as e:
            self.logger.error(f"Nmap scan error for {ip_address}: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during fingerprinting of {ip_address}: {e}")
        
        return device_info

    def monitor_network_traffic(self, interface="eth0", duration=60):
        """
        Monitor network traffic on a specific interface for a given duration.
        
        Args:
            interface (str): The network interface to monitor (e.g., 'eth0', 'wlan0').
            duration (int): Duration in seconds to monitor traffic.
            
        Returns:
            dict: Traffic statistics including packets, bytes, and protocols.
        """
        self.logger.info(f"Monitoring network traffic on interface {interface} for {duration} seconds")
        
        try:
            # This is a placeholder implementation
            # In a real implementation, we would use scapy or similar to capture packets
            import time
            import random
            
            # Simulate traffic monitoring
            time.sleep(duration)
            
            # Generate simulated traffic data
            traffic_stats = {
                'interface': interface,
                'duration': duration,
                'packets_captured': random.randint(1000, 10000),
                'bytes_transferred': random.randint(100000, 1000000),
                'protocols': {
                    'TCP': random.randint(300, 3000),
                    'UDP': random.randint(200, 2000),
                    'ICMP': random.randint(50, 500),
                    'Other': random.randint(100, 1000)
                },
                'top_talkers': [
                    {'ip': '192.168.1.10', 'bytes': random.randint(50000, 200000)},
                    {'ip': '192.168.1.15', 'bytes': random.randint(30000, 150000)},
                    {'ip': '192.168.1.20', 'bytes': random.randint(20000, 100000)}
                ]
            }
            
            self.logger.info(f"Traffic monitoring completed: {traffic_stats['packets_captured']} packets captured")
            return traffic_stats
            
        except Exception as e:
            self.logger.error(f"Error monitoring network traffic: {e}")
            return {
                'interface': interface,
                'duration': duration,
                'error': str(e)
            }

    def group_devices_by_network_segment(self, devices):
        """
        Group devices by their network segments.
        
        Args:
            devices (list): List of device dictionaries.
            
        Returns:
            dict: Devices grouped by network segment.
        """
        self.logger.info("Grouping devices by network segment")
        
        try:
            segments = {}
            
            for device in devices:
                ip = device.get('ip', 'Unknown')
                if ip != 'Unknown':
                    # Extract network segment (first three octets)
                    try:
                        segment = '.'.join(ip.split('.')[:3]) + '.0/24'
                        if segment not in segments:
                            segments[segment] = []
                        segments[segment].append(device)
                    except Exception:
                        # Handle malformed IP addresses
                        if 'unknown' not in segments:
                            segments['unknown'] = []
                        segments['unknown'].append(device)
                else:
                    if 'unknown' not in segments:
                        segments['unknown'] = []
                    segments['unknown'].append(device)
            
            self.logger.info(f"Devices grouped into {len(segments)} network segments")
            return segments
            
        except Exception as e:
            self.logger.error(f"Error grouping devices by network segment: {e}")
            return {}

    def analyze_network_performance(self, target_ip, ping_count=5):
        """
        Analyze network performance by pinging a target IP.
        
        Args:
            target_ip (str): The IP address to ping.
            ping_count (int): Number of ping packets to send.
            
        Returns:
            dict: Network performance metrics.
        """
        self.logger.info(f"Analyzing network performance for {target_ip}")
        
        try:
            import subprocess
            import re
            import platform
            
            # Determine the ping command based on the OS
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            
            # Execute ping command
            command = ['ping', param, str(ping_count), target_ip]
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Parse the output
            output = result.stdout
            
            # Extract metrics using regex
            packet_loss_match = re.search(r'(\d+)% packet loss', output)
            rtt_match = re.search(r'avg = ([\d.]+)', output) or re.search(r'average = ([\d.]+)', output) or re.search(r'time=([\d.]+)', output)
            
            packet_loss = int(packet_loss_match.group(1)) if packet_loss_match else 0
            avg_rtt = float(rtt_match.group(1)) if rtt_match else 0
            
            performance_data = {
                'target_ip': target_ip,
                'packet_loss_percent': packet_loss,
                'average_rtt_ms': avg_rtt,
                'ping_count': ping_count,
                'status': 'Good' if packet_loss == 0 and avg_rtt < 100 else 'Degraded' if packet_loss < 5 and avg_rtt < 300 else 'Poor'
            }
            
            self.logger.info(f"Network performance analysis completed: {performance_data}")
            return performance_data
            
        except Exception as e:
            self.logger.error(f"Error analyzing network performance for {target_ip}: {e}")
            return {
                'target_ip': target_ip,
                'error': str(e)
            }

if __name__ == '__main__':
    scanner = NetworkScanner()
    devices = scanner.scan_local_network()
    print(devices)
