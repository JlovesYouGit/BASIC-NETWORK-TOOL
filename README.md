# Network Management Tool

A comprehensive network scanning and device management tool that allows you to discover, analyze, and manage devices on your network.

## Features

- **Network Scanning**: Discover devices on local, server, and web networks
- **Device Fingerprinting**: Identify operating systems, open ports, and running services
- **Device Management**: Securely access and manage network devices
- **Interactive Dashboard**: Rich command-line interface for viewing and selecting devices
- **Enhanced Terminal Dashboard**: Advanced terminal UI with charts and visualizations
- **Web Interface**: Graphical web-based interface for network management
- **Network Access Control**: Block and unblock devices from accessing the network
- **Security Hardening**: Implements secure authentication and communication practices
- **SSH Key Auto-Detection**: Automatically detects SSH keys based on IP and hostname
- **Proper MAC Address Handling**: Displays "Unknown" for devices with undetermined MAC addresses

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Nmap on your system (required for device fingerprinting):
   - Windows: Download from https://nmap.org/download.html
   - macOS: `brew install nmap`
   - Linux: `sudo apt install nmap`

## Usage

### Command Line Interface

``bash
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

# Launch enhanced terminal dashboard
python network_tool.py --enhanced-dashboard
```

### Web Interface

To use the web-based interface:

```bash
# Run the web interface
python run_web.py

# Access the dashboard at: http://localhost:5000
```

### Dual Interface Launcher

For convenience, two batch files are provided to launch both interfaces simultaneously:

1. **Simple Launcher**: [run_dual_interface.bat](file:///C:/Users/JJ/Downloads/New%20folder%20(6)/project/run_dual_interface.bat) - Opens both interfaces in separate terminals
2. **Advanced Launcher**: [run_dual_interface_advanced.bat](file:///C:/Users/JJ/Downloads/New%20folder%20(6)/project/run_dual_interface_advanced.bat) - Opens both interfaces with a menu system for the CLI

To use either launcher:
```bash
# Double-click on the batch file in Windows Explorer
# Or run from command line:
run_dual_interface.bat
# or
run_dual_interface_advanced.bat
```

### SSH Key Auto-Detection

The tool now supports automatic SSH key detection:
- Select "auto" authentication method to automatically find and use appropriate SSH keys
- The system looks for keys based on the target device's IP address and hostname
- Supports standard SSH key locations and hostname/IP-specific keys

### MAC Address Handling

The tool properly handles and displays unknown MAC addresses:
- Devices with undetermined MAC addresses show "Unknown" instead of blank or N/A
- Consistent display across all interfaces (CLI, interactive dashboard, enhanced terminal dashboard)
- Improved user experience when MAC addresses cannot be determined

### Network Access Control

The tool now includes network access control features that allow you to block and unblock devices directly from both the command-line interface and the web interface:

```bash
# Block a device from network access (requires admin/root privileges)
python network_tool.py --block-device 192.168.1.100

# Unblock a device and restore network access (requires admin/root privileges)
python network_tool.py --unblock-device 192.168.1.100
```

In the web interface:
1. Navigate to the device list
2. Click the "Block" button on any device card to block network access
3. Blocked devices will show a "BLOCKED" badge and red border
4. Click the "Unblock" button to restore network access

The network access control works by using actual system firewall commands to create real blocking rules that prevent devices from communicating on the network. **Important**: The system now provides real network access control (not simulation) using platform-specific firewall commands:
- Windows: Uses `netsh advfirewall firewall` commands
- Linux: Uses `iptables` commands
- macOS/Unix: Uses `pfctl` commands

**Note**: Blocking operations require administrator/root privileges to execute.

**Persistent Blocking**: Blocked IP addresses are now stored in a persistent file (`blocked_ips.json`) and automatically restored on system startup. This ensures that blocked devices remain blocked even after system reboots.

## Project Structure

```
project/
├── src/
│   ├── network_tool.py          # Main application entry point
│   ├── modules/                 # Core functionality modules
│   │   ├── __init__.py
│   │   ├── scanner.py           # Network scanning capabilities
│   │   ├── manager.py           # Device management functions
│   │   ├── dashboard.py         # Interactive dashboard interface
│   │   └── enhanced_dashboard.py # Enhanced terminal dashboard
│   ├── web/                     # Web interface components
│   │   ├── app.py               # Flask web application
│   │   ├── templates/           # HTML templates
│   │   └── static/              # Static files (CSS, JS, images)
│   └── utils/                   # Utility functions
│       └── __init__.py
├── tests/                       # Unit tests
├── docs/                        # Documentation
├── requirements.txt             # Python dependencies
├── run_web.py                   # Web interface run script
├── run_dual_interface.bat       # Simple dual interface launcher
├── run_dual_interface_advanced.bat # Advanced dual interface launcher
└── README.md                    # This file
```

## Development

This project is organized according to the task list in the documentation:

### Phase 1: Basic Tool Implementation
1. Initial Network Scanning
2. Device Access (SSH)
3. Device Management
4. Server Network Scanning
5. Web Server Integration
6. Command-Line Interface
7. Error Handling and Logging
8. Demonstration

### Phase 2: Advanced Enhancements
9. Advanced Device Fingerprinting
10. Interactive Device Dashboard
11. Detailed Device View and Management
12. Security Hardening

### Future Enhancements
13. Web-based Dashboard using Flask
14. Database integration for persistent storage
15. REST API for remote access
16. Advanced analytics and reporting
17. Containerization support (Docker)
18. Integration with actual firewall APIs (iptables, pfSense, etc.)
19. Time-based blocking with automatic expiration
20. Blocking based on MAC address in addition to IP

## Security

This tool implements security best practices as outlined in the security hardening documentation. For production use, ensure you follow all security guidelines and use secure authentication methods.

## Enhanced Terminal Dashboard (blessed-contrib style)

For the enhanced terminal dashboard, we've implemented a Python-based solution that provides similar functionality to blessed-contrib:

- Network overview with statistics
- Device discovery with visual charts
- Performance metrics with ASCII charts
- Device management interface
- Progress indicators and spinners

The enhanced dashboard uses:
- **blessed**: For terminal handling
- **plotext**: For ASCII charting
- **rich**: For enhanced terminal UI components

To run the enhanced dashboard:
```bash
python network_tool.py --enhanced-dashboard
```