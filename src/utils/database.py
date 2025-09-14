"""
Database utility for Network Management Tool
"""

import sqlite3
import json
import os
from datetime import datetime

class NetworkDatabase:
    """Database utility for storing network scan results"""
    
    def __init__(self, db_path='network_data.db'):
        """Initialize the database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create devices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                mac_address TEXT,
                hostname TEXT,
                operating_system TEXT,
                scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                device_info TEXT
            )
        ''')
        
        # Create scan_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_type TEXT NOT NULL,
                scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                results TEXT
            )
        ''')
        
        # Create ports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                port_number INTEGER,
                service TEXT,
                version TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_device(self, device_info):
        """Save device information to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert or update device information
            cursor.execute('''
                INSERT OR REPLACE INTO devices 
                (ip_address, mac_address, hostname, operating_system, device_info)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                device_info.get('ip'),
                device_info.get('mac'),
                device_info.get('hostname'),
                device_info.get('os'),
                json.dumps(device_info)
            ))
            
            # Get the device ID
            device_id = cursor.lastrowid
            
            # Save port information if available
            if 'ports' in device_info:
                for port_info in device_info['ports']:
                    cursor.execute('''
                        INSERT INTO ports 
                        (device_id, port_number, service, version)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        device_id,
                        port_info.get('port'),
                        port_info.get('service'),
                        port_info.get('version')
                    ))
            
            conn.commit()
            return device_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def save_scan_results(self, scan_type, results):
        """Save scan results to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO scan_results 
                (scan_type, results)
                VALUES (?, ?)
            ''', (
                scan_type,
                json.dumps(results)
            ))
            
            scan_id = cursor.lastrowid
            conn.commit()
            return scan_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_devices(self):
        """Retrieve all devices from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM devices ORDER BY scan_timestamp DESC')
        rows = cursor.fetchall()
        
        devices = []
        for row in rows:
            device = {
                'id': row[0],
                'ip': row[1],
                'mac': row[2],
                'hostname': row[3],
                'os': row[4],
                'scan_timestamp': row[5],
                'device_info': json.loads(row[6]) if row[6] else {}
            }
            devices.append(device)
        
        conn.close()
        return devices
    
    def get_device_by_ip(self, ip_address):
        """Retrieve a specific device by IP address"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM devices WHERE ip_address = ?', (ip_address,))
        row = cursor.fetchone()
        
        if row:
            device = {
                'id': row[0],
                'ip': row[1],
                'mac': row[2],
                'hostname': row[3],
                'os': row[4],
                'scan_timestamp': row[5],
                'device_info': json.loads(row[6]) if row[6] else {}
            }
            return device
        
        conn.close()
        return None
    
    def get_scan_history(self):
        """Retrieve scan history from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM scan_results ORDER BY scan_timestamp DESC')
        rows = cursor.fetchall()
        
        scans = []
        for row in rows:
            scan = {
                'id': row[0],
                'scan_type': row[1],
                'scan_timestamp': row[2],
                'results': json.loads(row[3]) if row[3] else []
            }
            scans.append(scan)
        
        conn.close()
        return scans
    
    def get_device_ports(self, device_id):
        """Retrieve port information for a specific device"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ports WHERE device_id = ?', (device_id,))
        rows = cursor.fetchall()
        
        ports = []
        for row in rows:
            port = {
                'id': row[0],
                'device_id': row[1],
                'port': row[2],
                'service': row[3],
                'version': row[4]
            }
            ports.append(port)
        
        conn.close()
        return ports
    
    def delete_device(self, ip_address):
        """Delete a device from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM devices WHERE ip_address = ?', (ip_address,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

# Example usage
if __name__ == '__main__':
    # Create database instance
    db = NetworkDatabase()
    
    # Example device data
    device_data = {
        'ip': '192.168.1.100',
        'mac': '00:11:22:33:44:55',
        'hostname': 'test-device',
        'os': 'Linux',
        'ports': [
            {'port': 22, 'service': 'ssh', 'version': 'OpenSSH 7.9'},
            {'port': 80, 'service': 'http', 'version': 'Apache 2.4.41'}
        ]
    }
    
    # Save device to database
    device_id = db.save_device(device_data)
    print(f"Device saved with ID: {device_id}")
    
    # Retrieve devices
    devices = db.get_devices()
    print(f"Retrieved {len(devices)} devices")
    
    # Retrieve specific device
    device = db.get_device_by_ip('192.168.1.100')
    print(f"Retrieved device: {device}")