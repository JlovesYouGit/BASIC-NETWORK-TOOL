"""
Flask web application for Network Management Tool
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.scanner import NetworkScanner
from modules.manager import DeviceManager
from utils.database import NetworkDatabase

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Initialize the network scanner, device manager, and database
    scanner = NetworkScanner()
    manager = DeviceManager()
    database = NetworkDatabase()
    
    @app.route('/')
    def index():
        """Render the main dashboard page."""
        return render_template('index.html')
    
    @app.route('/api/scan/local')
    def scan_local():
        """API endpoint to scan local network."""
        try:
            devices = scanner.scan_local_network()
            # Save scan results to database
            database.save_scan_results('local', devices)
            return jsonify({'status': 'success', 'devices': devices})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/scan/server')
    def scan_server():
        """API endpoint to scan server network."""
        try:
            devices = scanner.scan_server_network()
            # Save scan results to database
            database.save_scan_results('server', devices)
            # Save individual devices to database
            for device in devices:
                database.save_device(device)
            return jsonify({'status': 'success', 'devices': devices})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/scan/web')
    def scan_web():
        """API endpoint to scan web server."""
        try:
            devices = scanner.scan_web_server()
            # Save scan results to database
            database.save_scan_results('web', devices)
            # Save individual devices to database
            for device in devices:
                database.save_device(device)
            return jsonify({'status': 'success', 'devices': devices})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/device/<ip>/fingerprint')
    def fingerprint_device(ip):
        """API endpoint to fingerprint a specific device."""
        try:
            device_info = scanner.fingerprint_device(ip)
            # Save device info to database
            database.save_device(device_info)
            return jsonify({'status': 'success', 'device': device_info})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/device/<ip>/manage', methods=['POST'])
    def manage_device(ip):
        """API endpoint to manage a specific device."""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'status': 'error', 'message': 'Username and password required'})
            
            result = manager.secure_manage_device(ip, username, password)
            return jsonify({'status': 'success', 'result': result})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/device/<ip>/block', methods=['POST'])
    def block_device(ip):
        """API endpoint to block a device's network access."""
        try:
            # Even if device is not reachable, we should still block it
            # Check if device is reachable (for informational purposes only)
            if not manager.is_device_reachable(ip):
                print(f"Device {ip} is not reachable, but will still be blocked")
                # We don't return an error here - we still want to block the device
            
            result = manager.block_device_network_access(ip)
            if result:
                return jsonify({'status': 'success', 'message': f'Device {ip} has been blocked'})
            else:
                return jsonify({'status': 'error', 'message': f'Failed to block device {ip}'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/device/<ip>/unblock', methods=['POST'])
    def unblock_device(ip):
        """API endpoint to unblock a device's network access."""
        try:
            # Even if device is not reachable, we should still unblock it
            # Check if device is reachable (for informational purposes only)
            if not manager.is_device_reachable(ip):
                print(f"Device {ip} is not reachable, but will still be unblocked")
                # We don't return an error here - we still want to unblock the device
            
            result = manager.unblock_device_network_access(ip)
            if result:
                return jsonify({'status': 'success', 'message': f'Device {ip} has been unblocked'})
            else:
                return jsonify({'status': 'error', 'message': f'Failed to unblock device {ip}'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/devices')
    def get_devices():
        """API endpoint to get all devices from database."""
        try:
            devices = database.get_devices()
            return jsonify({'status': 'success', 'devices': devices})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    @app.route('/api/scan/history')
    def get_scan_history():
        """API endpoint to get scan history from database."""
        try:
            scans = database.get_scan_history()
            return jsonify({'status': 'success', 'scans': scans})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)