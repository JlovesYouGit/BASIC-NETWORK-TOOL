# Network Management Tool - API Documentation

This document provides an overview of the Network Management Tool API and references to detailed documentation for each module.

## Overview

The Network Management Tool provides a comprehensive set of APIs for network scanning, device management, and interactive dashboard functionality. The tool is organized into three main modules:

1. [NetworkScanner](api_scanner.md) - Network scanning capabilities
2. [DeviceManager](api_manager.md) - Device management functionality
3. [InteractiveDashboard](api_dashboard.md) - Interactive dashboard interface

## Module Documentation

### NetworkScanner Module
The NetworkScanner module provides network scanning capabilities for local, server, and web networks.

[View detailed NetworkScanner API documentation](api_scanner.md)

### DeviceManager Module
The DeviceManager module provides device management capabilities including SSH access and network interface control.

[View detailed DeviceManager API documentation](api_manager.md)

### InteractiveDashboard Module
The InteractiveDashboard module provides an interactive dashboard for network device management using the Rich library for enhanced visualization.

[View detailed InteractiveDashboard API documentation](api_dashboard.md)

## Main Application Interface

The main application interface is provided through the command-line interface in `network_tool.py`. The following commands are available:

```bash
# Scan local network
python network_tool.py --scan local

# Scan server network
python network_tool.py --scan server

# Scan web server
python network_tool.py --scan web

# Manage a specific device
python network_tool.py --manage 192.168.1.100

# Launch interactive dashboard
python network_tool.py --dashboard
```

## Usage Examples

### Basic Network Scanning
```python
from modules.scanner import NetworkScanner

scanner = NetworkScanner()
devices = scanner.scan_local_network("192.168.1.0/24")
for device in devices:
    print(f"Found device: {device['ip']} with MAC {device.get('mac', 'Unknown')}")
```

### Device Management
```python
from modules.manager import DeviceManager

manager = DeviceManager()
manager.manage_device("192.168.1.10", "admin", "password123")
```

### Interactive Dashboard
```python
from modules.scanner import NetworkScanner
from modules.manager import DeviceManager
from modules.dashboard import InteractiveDashboard

scanner = NetworkScanner()
manager = DeviceManager()
dashboard = InteractiveDashboard(scanner, manager)
dashboard.run()
```

## Error Handling

All modules include comprehensive error handling and logging. Exceptions are caught and logged appropriately, with user-friendly error messages provided where applicable.

## Dependencies

The API requires the following Python packages:
- scapy>=2.4.5
- paramiko>=2.7.2
- python-nmap>=0.6.1
- rich>=10.0.0

Additionally, the Nmap executable must be installed on the system for advanced fingerprinting capabilities.