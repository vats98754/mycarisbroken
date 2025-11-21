#!/usr/bin/env python3
"""
OBD-II Data Collection Server for Raspberry Pi
Streams real-time vehicle data over WebSocket to connected clients
"""

import obd
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import json
import logging
from datetime import datetime
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'obd-realtime-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
connection = None
running = False
data_thread = None
db_path = 'obd_data.db'

# Define the OBD commands we want to monitor
MONITORED_COMMANDS = [
    ('RPM', obd.commands.RPM),
    ('SPEED', obd.commands.SPEED),
    ('ENGINE_LOAD', obd.commands.ENGINE_LOAD),
    ('COOLANT_TEMP', obd.commands.COOLANT_TEMP),
    ('INTAKE_TEMP', obd.commands.INTAKE_TEMP),
    ('THROTTLE_POS', obd.commands.THROTTLE_POS),
    ('MAF', obd.commands.MAF),
    ('INTAKE_PRESSURE', obd.commands.INTAKE_PRESSURE),
    ('FUEL_PRESSURE', obd.commands.FUEL_PRESSURE),
    ('TIMING_ADVANCE', obd.commands.TIMING_ADVANCE),
    ('FUEL_LEVEL', obd.commands.FUEL_LEVEL),
    ('BAROMETRIC_PRESSURE', obd.commands.BAROMETRIC_PRESSURE),
    ('AMBIANT_AIR_TEMP', obd.commands.AMBIANT_AIR_TEMP),
    ('RUN_TIME', obd.commands.RUN_TIME),
]


def init_database():
    """Initialize SQLite database for storing OBD readings"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table for storing OBD readings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obd_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            rpm REAL,
            speed REAL,
            engine_load REAL,
            coolant_temp REAL,
            intake_temp REAL,
            throttle_pos REAL,
            maf REAL,
            intake_pressure REAL,
            fuel_pressure REAL,
            timing_advance REAL,
            fuel_level REAL,
            barometric_pressure REAL,
            ambient_air_temp REAL,
            run_time REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized")


def store_reading(data):
    """Store a reading in the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO obd_readings (
                rpm, speed, engine_load, coolant_temp, intake_temp,
                throttle_pos, maf, intake_pressure, fuel_pressure,
                timing_advance, fuel_level, barometric_pressure,
                ambient_air_temp, run_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('RPM'),
            data.get('SPEED'),
            data.get('ENGINE_LOAD'),
            data.get('COOLANT_TEMP'),
            data.get('INTAKE_TEMP'),
            data.get('THROTTLE_POS'),
            data.get('MAF'),
            data.get('INTAKE_PRESSURE'),
            data.get('FUEL_PRESSURE'),
            data.get('TIMING_ADVANCE'),
            data.get('FUEL_LEVEL'),
            data.get('BAROMETRIC_PRESSURE'),
            data.get('AMBIANT_AIR_TEMP'),
            data.get('RUN_TIME')
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error storing reading: {e}")


def connect_obd():
    """Establish connection to OBD-II adapter"""
    global connection
    
    logger.info("Attempting to connect to OBD-II adapter...")
    
    # Try to connect (adjust parameters for Bluetooth adapters if needed)
    try:
        connection = obd.Async(fast=False, timeout=30)  # Async mode for continuous monitoring
        
        if connection.is_connected():
            logger.info(f"Connected to OBD-II adapter")
            logger.info(f"Protocol: {connection.protocol_name()}")
            logger.info(f"Supported commands: {len(connection.supported_commands)}")
            
            # Watch all monitored commands
            for name, cmd in MONITORED_COMMANDS:
                if connection.supports(cmd):
                    connection.watch(cmd)
                    logger.info(f"Watching: {name}")
                else:
                    logger.warning(f"Command not supported: {name}")
            
            # Start the async connection
            connection.start()
            return True
        else:
            logger.error("Failed to connect to OBD-II adapter")
            return False
            
    except Exception as e:
        logger.error(f"Error connecting to OBD: {e}")
        return False


def collect_data():
    """Continuously collect OBD data and broadcast to clients"""
    global running, connection
    
    logger.info("Starting data collection thread")
    
    while running:
        try:
            if connection and connection.is_connected():
                data = {
                    'timestamp': datetime.now().isoformat(),
                }
                
                # Query all monitored commands
                for name, cmd in MONITORED_COMMANDS:
                    if connection.supports(cmd):
                        response = connection.query(cmd)
                        if not response.is_null():
                            # Convert value to float if it has magnitude (Pint quantity)
                            if hasattr(response.value, 'magnitude'):
                                data[name] = float(response.value.magnitude)
                            else:
                                data[name] = response.value
                        else:
                            data[name] = None
                    else:
                        data[name] = None
                
                # Broadcast to all connected clients
                socketio.emit('obd_data', data, namespace='/')
                
                # Store in database (every reading)
                store_reading(data)
                
                # Log summary
                logger.debug(f"RPM: {data.get('RPM')}, Speed: {data.get('SPEED')}")
                
            else:
                logger.warning("OBD connection lost, attempting reconnect...")
                if connect_obd():
                    logger.info("Reconnected successfully")
                else:
                    time.sleep(5)  # Wait before retry
                    
        except Exception as e:
            logger.error(f"Error in data collection: {e}")
        
        # Adjust this delay for update frequency (0.5 = 2 updates/sec)
        time.sleep(0.5)


@app.route('/')
def index():
    """Serve the dashboard"""
    return render_template('dashboard.html')


@app.route('/api/connection_status')
def connection_status():
    """Return current OBD connection status"""
    if connection and connection.is_connected():
        return {
            'connected': True,
            'protocol': connection.protocol_name(),
            'supported_commands': len(connection.supported_commands)
        }
    return {'connected': False}


@app.route('/api/supported_commands')
def supported_commands():
    """Return list of supported OBD commands"""
    if connection and connection.is_connected():
        commands_list = []
        for cmd in connection.supported_commands:
            commands_list.append({
                'name': cmd.name,
                'description': cmd.desc,
                'command': cmd.command.decode('utf-8') if isinstance(cmd.command, bytes) else cmd.command
            })
        return {'commands': commands_list}
    return {'commands': []}


@app.route('/api/export_csv')
def export_csv():
    """Export database to CSV"""
    import csv
    from flask import Response, stream_with_context
    import io
    
    def generate():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM obd_readings ORDER BY timestamp DESC LIMIT 10000')
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        
        for row in cursor.fetchall():
            writer.writerow(row)
            
        conn.close()
        return output.getvalue()
    
    return Response(
        generate(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=obd_data.csv'}
    )


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connection_response', {'data': 'Connected to OBD server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


@socketio.on('start_monitoring')
def handle_start():
    """Start OBD monitoring"""
    global running, data_thread
    
    if not running:
        if connect_obd():
            running = True
            data_thread = threading.Thread(target=collect_data)
            data_thread.daemon = True
            data_thread.start()
            emit('status', {'message': 'Monitoring started'})
        else:
            emit('status', {'message': 'Failed to connect to OBD adapter', 'error': True})


@socketio.on('stop_monitoring')
def handle_stop():
    """Stop OBD monitoring"""
    global running, connection
    
    running = False
    if connection:
        connection.stop()
        connection.close()
    emit('status', {'message': 'Monitoring stopped'})


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("OBD-II Real-Time Data Collection Server")
    logger.info("=" * 60)
    
    # Initialize database
    init_database()
    
    # Get local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    logger.info(f"Starting server on {local_ip}:5000")
    logger.info("Access the dashboard from your Mac at:")
    logger.info(f"  http://{local_ip}:5000")
    logger.info("")
    logger.info("To find Raspberry Pi IP, run: hostname -I")
    logger.info("=" * 60)
    
    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
