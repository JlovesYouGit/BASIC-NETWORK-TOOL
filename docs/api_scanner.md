# NetworkScanner API Documentation

This document provides detailed API documentation for the NetworkScanner module.

## Class: NetworkScanner

The NetworkScanner class provides network scanning capabilities for local, server, and web networks.

### Constructor

```python
NetworkScanner()
```

Initializes a new instance of the NetworkScanner class.

### Methods

#### scan_local_network

```python
scan_local_network(ip_range="192.168.1.0/24")
```

Scans a local network for connected devices using ARP requests.

**Parameters:**
- `ip_range` (str): The IP range to scan (e.g., "192.168.1.0/24"). Defaults to "192.168.1.0/24".

**Returns:**
- `list`: A list of dictionaries, where each dictionary contains the 'ip' and 'mac' address of a device.

**Example:**
```python
scanner = NetworkScanner()
devices = scanner.scan_local_network("192.168.1.0/24")
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device.get('mac', 'Unknown')}")
```

#### scan_server_network

```python
scan_server_network(target="192.168.1.0/24", ports=[22, 80, 443, 3389])
```

Scans a server network for connected devices using port scanning.

**Parameters:**
- `target` (str): The target IP range or hostname to scan. Defaults to "192.168.1.0/24".
- `ports` (list): List of ports to scan for open services. Defaults to [22, 80, 443, 3389].

**Returns:**
- `list`: A list of dictionaries containing device information including IP, MAC, hostname, OS, and open ports.

**Example:**
```python
scanner = NetworkScanner()
devices = scanner.scan_server_network("10.0.0.0/24", [22, 80, 443])
for device in devices:
    print(f"IP: {device['ip']}, OS: {device['os']}")
```

#### scan_web_server

```python
scan_web_server(target="example.com")
```

Scans a web server for connected devices and services.

**Parameters:**
- `target` (str): The target web server hostname or IP address. Defaults to "example.com".

**Returns:**
- `list`: A list of dictionaries containing device information including IP, hostname, OS, and open ports.

**Example:**
```python
scanner = NetworkScanner()
devices = scanner.scan_web_server("google.com")
for device in devices:
    print(f"IP: {device['ip']}, Hostname: {device['hostname']}")
```

#### fingerprint_device

```python
fingerprint_device(ip_address)
```

Performs detailed fingerprinting of a device using Nmap.

**Parameters:**
- `ip_address` (str): The IP address of the device to scan.

**Returns:**
- `dict`: A dictionary containing detailed information about the device including IP, OS, hostname, and open ports with services.

**Example:**
```python
scanner = NetworkScanner()
device_info = scanner.fingerprint_device("192.168.1.1")
print(f"OS: {device_info['os']}")
for port in device_info['ports']:
    print(f"Port {port['port']}: {port['service']} {port['version']}")
```

### Private Methods

#### _ping_scan

```python
_ping_scan(target)
```

Performs a basic ICMP ping scan as fallback.

**Parameters:**
- `target` (str): The target IP range to scan.

**Returns:**
- `list`: A list of dictionaries containing device information.

#### _web_port_scan

```python
_web_port_scan(target)
```

Performs a basic port scan for common web services as fallback.

**Parameters:**
- `target` (str): The target hostname or IP address.

**Returns:**
- `list`: A list of dictionaries containing device information.

#### _get_service_name

```python
_get_service_name(port)
```

Returns a service name for a given port number.

**Parameters:**
- `port` (int): The port number.

**Returns:**
- `str`: The service name.