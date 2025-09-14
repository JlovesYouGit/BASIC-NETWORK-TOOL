# SSH Key Auto-Detection Feature

This document describes the automatic SSH key detection feature implemented in the Network Management Tool.

## Overview

The Network Management Tool now includes an enhanced automatic SSH key detection feature that can automatically find and use appropriate SSH keys based on the target device's IP address, hostname detected from the system, and device information. This feature enhances security and usability by reducing the need for manual key path specification.

## How It Works

### 1. Device Information Gathering
The system first gathers detailed information about the target device through fingerprinting, including:
- IP address
- Hostname (detected from the actual system, not example.com)
- Operating system
- Open ports and services

### 2. Hostname Resolution
The system attempts to resolve the hostname of the target IP address using reverse DNS lookup to get the actual hostname from the system.

### 3. Key Path Generation
Based on the device information, the system generates a prioritized list of potential SSH key paths:

1. **Keys based on device information from fingerprinting** (highest priority):
   - Hostname from device info: `~/.ssh/id_rsa_{device_hostname}`
   - OS-specific keys: `~/.ssh/id_rsa_linux`, `~/.ssh/id_rsa_windows`, `~/.ssh/id_rsa_macos`

2. **Device-specific keys based on hostname from DNS resolution** (high priority):
   - `~/.ssh/id_rsa_{hostname}`
   - `~/.ssh/id_dsa_{hostname}`
   - `~/.ssh/id_ecdsa_{hostname}`
   - `~/.ssh/id_ed25519_{hostname}`

3. **Device-specific keys based on IP address**:
   - `~/.ssh/id_rsa_{ip_with_underscores}`
   - `~/.ssh/id_dsa_{ip_with_underscores}`
   - `~/.ssh/id_ecdsa_{ip_with_underscores}`
   - `~/.ssh/id_ed25519_{ip_with_underscores}`

4. **Standard SSH key locations** (lowest priority):
   - `~/.ssh/id_rsa`
   - `~/.ssh/id_dsa`
   - `~/.ssh/id_ecdsa`
   - `~/.ssh/id_ed25519`

### 4. Key Selection
The system checks for the existence of each key in order of priority and uses the first one found.

## Usage

### Command Line Interface
```bash
# Use auto-detection (now enhanced with actual device hostname)
python network_tool.py --manage 192.168.1.100
# When prompted, select "auto" authentication method
# The system will automatically gather device information including the actual hostname and find appropriate keys

# Or explicitly use key with auto-detection
python network_tool.py --manage 192.168.1.100
# When prompted, select "key" authentication method and press Enter for auto-detection
```

### Interactive Dashboards
In both the regular and enhanced dashboards:
1. When managing a device, select "auto" authentication method
2. Or select "key" authentication method and press Enter when prompted for the key path
3. The system will automatically gather device information including the actual hostname and find appropriate keys

## Security Considerations

1. **Private Key Protection**: The system only accesses keys that already exist in the user's `.ssh` directory
2. **No Key Creation**: The system does not create new keys, only uses existing ones
3. **Secure Storage**: Keys remain in their original secure locations
4. **Access Control**: The system respects file system permissions on SSH keys
5. **Hostname Resolution**: DNS lookups are cached to avoid repeated queries

## Configuration

No additional configuration is required. The feature works automatically with standard SSH key locations.

## Troubleshooting

### No Key Found
If no key is found, the system will display an error message with suggestions:
1. Providing a specific key path
2. Ensuring SSH keys exist in `~/.ssh/` directory
3. Creating hostname or IP-specific keys for better organization
4. Suggested key names based on the device information

### Key Requires Password
If the SSH key requires a password, the system will indicate this and suggest using password authentication instead.

## Example Key Naming

For a device with IP `192.168.1.100`, actual hostname `webserver01.company.com`, and Linux OS:

```
~/.ssh/
├── id_rsa_webserver01.company.com  # Hostname from device info (highest priority)
├── id_rsa_webserver01.company.com  # Hostname from DNS resolution (high priority)
├── id_rsa_192_168_1_100           # IP-specific key
├── id_rsa_linux                   # OS-specific key
├── id_rsa                         # Standard key (used if no specific keys found)
└── id_ed25519                     # Alternative standard key
```

## Benefits

1. **Improved Usability**: Users don't need to remember or type key paths
2. **Better Organization**: Supports hostname, IP, and OS-specific key organization
3. **Security**: Encourages proper SSH key management practices
4. **Flexibility**: Still allows manual key specification when needed
5. **Cross-Platform**: Works on Windows, macOS, and Linux
6. **Intelligent Detection**: Uses actual device hostname detected from the system for more accurate key selection
7. **Performance**: Caches hostname resolutions to avoid repeated DNS lookups
8. **Real Hostname Detection**: Uses the actual hostname detected from the system, not example.com

## Limitations

1. Only works with existing SSH keys
2. Currently supports RSA, DSA, ECDSA, and Ed25519 key types
3. Requires keys to be in standard OpenSSH format
4. Device fingerprinting is required for enhanced detection (happens automatically)