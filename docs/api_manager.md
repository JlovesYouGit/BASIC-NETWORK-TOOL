# DeviceManager API Documentation

This document provides detailed API documentation for the DeviceManager module.

## Class: DeviceManager

The DeviceManager class provides device management capabilities including SSH access and network interface control.

### Constructor

```python
DeviceManager()
```

Initializes a new instance of the DeviceManager class.

### Methods

#### manage_device

```python
manage_device(ip_address, username, password)
```

Manage a device by temporarily disabling its network interface using password authentication.

**Parameters:**
- `ip_address` (str): The IP address of the device to manage.
- `username` (str): The username for SSH access.
- `password` (str): The password for SSH access.

**Returns:**
- None

**Example:**
```python
manager = DeviceManager()
manager.manage_device("192.168.1.10", "admin", "password123")
```

#### secure_manage_device

```python
secure_manage_device(ip_address, ssh_key_path, username='admin')
```

Securely manage a device using SSH key authentication.

**Parameters:**
- `ip_address` (str): The IP address of the device to manage.
- `ssh_key_path` (str): Path to the SSH private key file.
- `username` (str): The username for SSH access. Defaults to 'admin'.

**Returns:**
- None

**Example:**
```python
manager = DeviceManager()
manager.secure_manage_device("192.168.1.10", "/path/to/private_key", "admin")
```

#### test_connection

```python
test_connection(ip_address, username, password=None, ssh_key_path=None)
```

Test SSH connection to a device.

**Parameters:**
- `ip_address` (str): The IP address of the device to test.
- `username` (str): The username for SSH access.
- `password` (str, optional): The password for SSH access.
- `ssh_key_path` (str, optional): Path to the SSH private key file.

**Returns:**
- `bool`: True if connection successful, False otherwise.

**Example:**
```python
manager = DeviceManager()
# Test with password authentication
success = manager.test_connection("192.168.1.10", "admin", password="password123")
# Test with key authentication
success = manager.test_connection("192.168.1.10", "admin", ssh_key_path="/path/to/private_key")
```