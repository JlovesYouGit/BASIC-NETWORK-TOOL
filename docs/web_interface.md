# Web Interface for Network Management Tool

This document describes the web-based interface for the Network Management Tool, which provides a graphical user interface for network scanning and device management.

## Features

1. **Dashboard View**: Overview of network statistics and discovered devices
2. **Network Scanning**: Scan local, server, and web networks
3. **Device Management**: Manage devices through a web interface
4. **Device Fingerprinting**: Get detailed information about devices
5. **Responsive Design**: Works on desktop and mobile devices
6. **REST API**: Programmatic access to all functionality
7. **Database Integration**: Persistent storage of scan results and device information

## Technology Stack

- **Flask**: Web framework for Python
- **Flask-RESTful**: REST API framework
- **SQLite**: Lightweight database for persistent storage
- **Bootstrap 5**: Frontend framework for responsive design
- **jQuery**: JavaScript library for DOM manipulation
- **Font Awesome**: Icon library for UI elements

## Installation

1. Install the required dependencies:
   ```bash
   pip install flask flask-restful
   ```

2. Or install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Web Interface

To start the web interface, run:
```bash
python run_web.py
```

Then access the dashboard at: http://localhost:5000

## Running the REST API

To start the REST API, run:
```bash
python run_api.py
```

## API Endpoints

The web interface communicates with the backend through the following API endpoints:

### Web Interface Endpoints
- `GET /api/scan/local` - Scan local network
- `GET /api/scan/server` - Scan server network
- `GET /api/scan/web` - Scan web server
- `GET /api/device/<ip>/fingerprint` - Fingerprint a specific device
- `POST /api/device/<ip>/manage` - Manage a specific device
- `GET /api/devices` - Get all devices from database
- `GET /api/scan/history` - Get scan history from database

### REST API Endpoints
- `GET /api/scan/<local|server|web>` - Perform network scan
- `GET /api/device/<ip>/fingerprint` - Fingerprint a specific device
- `POST /api/device/<ip>/manage` - Manage a specific device
- `GET /api/devices` - Get all devices from database
- `GET /api/scan/history` - Get scan history from database

## Directory Structure

```
src/web/
├── app.py              # Flask web application
├── api.py              # REST API implementation
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   └── index.html      # Dashboard template
└── static/             # Static files
    └── css/
        └── style.css   # Custom CSS

src/utils/
├── database.py         # Database utility for persistent storage
```

## Database Schema

The application uses SQLite for persistent storage with the following tables:

1. **devices**: Stores information about discovered devices
2. **scan_results**: Stores complete scan results
3. **ports**: Stores port information for devices

## API Usage Examples

### Scan Local Network
```bash
curl http://localhost:5000/api/scan/local
```

### Fingerprint Device
```bash
curl http://localhost:5000/api/device/192.168.1.1/fingerprint
```

### Manage Device
```bash
curl -X POST http://localhost:5000/api/device/192.168.1.1/manage \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password", "action": "disable"}'
```

### Get All Devices
```bash
curl http://localhost:5000/api/devices
```

### Get Scan History
```bash
curl http://localhost:5000/api/scan/history
```

## Future Enhancements

Planned enhancements for the web interface include:

1. **User Authentication**: Secure login system
2. **Device Grouping**: Organize devices by type or location
3. **Advanced Analytics**: Charts and graphs for network data
4. **Real-time Updates**: WebSocket integration for live updates
5. **Mobile App**: Native mobile application
6. **Cloud Integration**: Store data in cloud services

## Security Considerations

- The web interface should only be accessible on trusted networks
- HTTPS should be used in production environments
- Proper authentication should be implemented for multi-user environments
- Input validation should be performed on all API endpoints

## Troubleshooting

If you encounter issues:

1. Ensure all dependencies are installed
2. Check that the Flask server is running
3. Verify network connectivity
4. Check the browser console for JavaScript errors
5. Review the server logs for backend errors