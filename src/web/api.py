"""
REST API for Network Management Tool
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.scanner import NetworkScanner
from modules.manager import DeviceManager
from utils.database import NetworkDatabase

class NetworkScannerAPI(Resource):
    """API for network scanning functionality"""
    
    def __init__(self):
        self.scanner = NetworkScanner()
        self.database = NetworkDatabase()
    
    def get(self, scan_type):
        """Perform a network scan"""
        try:
            if scan_type == 'local':
                devices = self.scanner.scan_local_network()
                # Save scan results to database
                self.database.save_scan_results('local', devices)
                return {'status': 'success', 'devices': devices}, 200
            elif scan_type == 'server':
                devices = self.scanner.scan_server_network()
                # Save scan results to database
                self.database.save_scan_results('server', devices)
                # Save individual devices to database
                for device in devices:
                    self.database.save_device(device)
                return {'status': 'success', 'devices': devices}, 200
            elif scan_type == 'web':
                devices = self.scanner.scan_web_server()
                # Save scan results to database
                self.database.save_scan_results('web', devices)
                # Save individual devices to database
                for device in devices:
                    self.database.save_device(device)
                return {'status': 'success', 'devices': devices}, 200
            else:
                return {'status': 'error', 'message': 'Invalid scan type'}, 400
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class DeviceFingerprintAPI(Resource):
    """API for device fingerprinting"""
    
    def __init__(self):
        self.scanner = NetworkScanner()
        self.database = NetworkDatabase()
    
    def get(self, ip_address):
        """Fingerprint a specific device"""
        try:
            device_info = self.scanner.fingerprint_device(ip_address)
            # Save device info to database
            self.database.save_device(device_info)
            return {'status': 'success', 'device': device_info}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class DeviceManagementAPI(Resource):
    """API for device management"""
    
    def __init__(self):
        self.manager = DeviceManager()
    
    def post(self, ip_address):
        """Manage a specific device"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            action = data.get('action', 'disable')
            
            if not username or not password:
                return {'status': 'error', 'message': 'Username and password required'}, 400
            
            if action == 'disable':
                result = self.manager.secure_manage_device(ip_address, username, password)
                return {'status': 'success', 'result': result}, 200
            else:
                return {'status': 'error', 'message': 'Invalid action'}, 400
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class DeviceBlockingAPI(Resource):
    """API for device network access control"""
    
    def __init__(self):
        self.manager = DeviceManager()
    
    def post(self, ip_address):
        """Block a device's network access"""
        try:
            # Even if device is not reachable, we should still block it
            # Check if device is reachable (for informational purposes only)
            if not self.manager.is_device_reachable(ip_address):
                print(f"Device {ip_address} is not reachable, but will still be blocked")
                # We don't return an error here - we still want to block the device
            
            result = self.manager.block_device_network_access(ip_address)
            if result:
                return {'status': 'success', 'message': f'Device {ip_address} has been blocked'}, 200
            else:
                return {'status': 'error', 'message': f'Failed to block device {ip_address}'}, 500
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class DeviceUnblockingAPI(Resource):
    """API for device network access control"""
    
    def __init__(self):
        self.manager = DeviceManager()
    
    def post(self, ip_address):
        """Unblock a device's network access"""
        try:
            # Even if device is not reachable, we should still unblock it
            # Check if device is reachable (for informational purposes only)
            if not self.manager.is_device_reachable(ip_address):
                print(f"Device {ip_address} is not reachable, but will still be unblocked")
                # We don't return an error here - we still want to unblock the device
            
            result = self.manager.unblock_device_network_access(ip_address)
            if result:
                return {'status': 'success', 'message': f'Device {ip_address} has been unblocked'}, 200
            else:
                return {'status': 'error', 'message': f'Failed to unblock device {ip_address}'}, 500
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class DevicesAPI(Resource):
    """API for retrieving devices from database"""
    
    def __init__(self):
        self.database = NetworkDatabase()
    
    def get(self):
        """Get all devices from database"""
        try:
            devices = self.database.get_devices()
            return {'status': 'success', 'devices': devices}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

class ScanHistoryAPI(Resource):
    """API for retrieving scan history from database"""
    
    def __init__(self):
        self.database = NetworkDatabase()
    
    def get(self):
        """Get scan history from database"""
        try:
            scans = self.database.get_scan_history()
            return {'status': 'success', 'scans': scans}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

def create_api_app():
    """Create and configure the Flask-RESTful API application."""
    app = Flask(__name__)
    api = Api(app)
    
    # Add API resources
    api.add_resource(NetworkScannerAPI, '/api/scan/<string:scan_type>')
    api.add_resource(DeviceFingerprintAPI, '/api/device/<string:ip_address>/fingerprint')
    api.add_resource(DeviceManagementAPI, '/api/device/<string:ip_address>/manage')
    api.add_resource(DeviceBlockingAPI, '/api/device/<string:ip_address>/block')
    api.add_resource(DeviceUnblockingAPI, '/api/device/<string:ip_address>/unblock')
    api.add_resource(DevicesAPI, '/api/devices')
    api.add_resource(ScanHistoryAPI, '/api/scan/history')
    
    return app

if __name__ == '__main__':
    app = create_api_app()
    print("Starting Network Management Tool REST API...")
    print("API endpoints:")
    print("  GET  /api/scan/<local|server|web>")
    print("  GET  /api/device/<ip>/fingerprint")
    print("  POST /api/device/<ip>/manage")
    print("  POST /api/device/<ip>/block")
    print("  POST /api/device/<ip>/unblock")
    print("  GET  /api/devices")
    print("  GET  /api/scan/history")
    print("Access the API at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)