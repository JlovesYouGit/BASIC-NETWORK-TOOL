# InteractiveDashboard API Documentation

This document provides detailed API documentation for the InteractiveDashboard module.

## Class: InteractiveDashboard

The InteractiveDashboard class provides an interactive dashboard for network device management using the Rich library for enhanced visualization.

### Constructor

```python
InteractiveDashboard(scanner, manager)
```

Initializes a new instance of the InteractiveDashboard class.

**Parameters:**
- `scanner` (NetworkScanner): The network scanner instance.
- `manager` (DeviceManager): The device manager instance.

**Example:**
```python
scanner = NetworkScanner()
manager = DeviceManager()
dashboard = InteractiveDashboard(scanner, manager)
```

### Methods

#### run

```python
run()
```

Run the interactive dashboard. This method starts the main dashboard loop that presents options to the user.

**Parameters:**
- None

**Returns:**
- None

**Example:**
```python
dashboard = InteractiveDashboard(scanner, manager)
dashboard.run()
```

#### _scan_and_display

```python
_scan_and_display(network_type)
```

Scan a network type and display results in a rich table format.

**Parameters:**
- `network_type` (str): The type of network to scan. Valid values are 'local', 'server', and 'web'.

**Returns:**
- None

**Example:**
```python
dashboard._scan_and_display('local')
```

#### _show_device_details

```python
_show_device_details(device)
```

Show detailed information about a device in a formatted table.

**Parameters:**
- `device` (dict): The device information dictionary containing IP, MAC, hostname, OS, and ports.

**Returns:**
- None

**Example:**
```python
device_info = {
    'ip': '192.168.1.10',
    'mac': '00:11:22:33:44:55',
    'hostname': 'test-host',
    'os': 'Linux',
    'ports': [
        {'port': 22, 'service': 'ssh', 'version': 'OpenSSH 7.9'},
        {'port': 80, 'service': 'http', 'version': 'Apache 2.4.41'}
    ]
}
dashboard._show_device_details(device_info)
```

#### _manage_device

```python
_manage_device(ip_address)
```

Manage a device by temporarily disabling its network interface. This method prompts the user for authentication details.

**Parameters:**
- `ip_address` (str): The IP address of the device to manage.

**Returns:**
- None

**Example:**
```python
dashboard._manage_device('192.168.1.10')
```