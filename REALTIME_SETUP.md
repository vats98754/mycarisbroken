# 🚗 OBD-II Real-Time Visualization System

A complete real-time vehicle diagnostics visualization system that streams OBD-II data from your Raspberry Pi to your Mac for live monitoring and data logging.

## 📋 System Overview

This system consists of two components:

1. **Raspberry Pi Server** (`obd_server.py`) - Connects to your car's OBD-II port via ELM327 adapter and streams data over your network
2. **Mac Dashboard Client** (Web Browser) - Beautiful real-time visualization with charts and metrics

### Features

- ✅ Real-time data streaming over WiFi/Network
- ✅ Interactive charts for RPM, Speed, Temperature, Load, etc.
- ✅ SQLite database for data logging
- ✅ CSV export functionality
- ✅ Automatic reconnection handling
- ✅ Support for 14+ OBD parameters
- ✅ Modern, responsive dashboard design

## 🔧 Hardware Requirements

### Raspberry Pi Setup
- Raspberry Pi (any model with network capability)
- ELM327 OBD-II Adapter (USB or Bluetooth)
- OBD-II port access to your vehicle
- Power source for Raspberry Pi

### Mac Setup
- Mac computer on the same network as Raspberry Pi
- Modern web browser (Chrome, Firefox, Safari)

## 📦 Installation

### Part 1: Raspberry Pi Setup

#### 1. Connect to Raspberry Pi via SSH
```bash
ssh pi@raspberrypi.local
# Default password is usually 'raspberry'
```

#### 2. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev git
```

#### 3. Clone or Transfer the Code
Option A - If using Git:
```bash
git clone <your-repo-url>
cd mycarisbroken
```

Option B - If transferring files manually:
```bash
# On your Mac, from the project directory:
scp -r /Users/anvayvats/mycarisbroken pi@raspberrypi.local:~/

# Then SSH into Pi:
ssh pi@raspberrypi.local
cd mycarisbroken
```

#### 4. Install Python Dependencies
```bash
pip3 install -r requirements_server.txt
```

#### 5. Connect OBD-II Adapter

**For USB Adapters:**
```bash
# Plug in the USB adapter
# Check if it's detected:
ls /dev/ttyUSB*
# You should see /dev/ttyUSB0 or similar
```

**For Bluetooth Adapters:**
```bash
# Pair the Bluetooth adapter first
sudo bluetoothctl
# In bluetoothctl:
scan on
# Wait for your OBD adapter to appear
pair XX:XX:XX:XX:XX:XX  # Replace with your adapter's MAC
connect XX:XX:XX:XX:XX:XX
exit

# Create serial port binding:
sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX
```

#### 6. Test OBD Connection
```bash
python3 -c "import obd; print(obd.scan_serial())"
# Should show available serial ports
```

#### 7. Start the Server
```bash
python3 obd_server.py
```

The server will display:
```
=============================================
OBD-II Real-Time Data Collection Server
Starting server on 192.168.1.XXX:5000
Access the dashboard from your Mac at:
  http://192.168.1.XXX:5000
=============================================
```

**Note the IP address!** You'll need this on your Mac.

#### 8. (Optional) Run Server on Startup
```bash
# Create systemd service
sudo nano /etc/systemd/system/obd-server.service
```

Add this content:
```ini
[Unit]
Description=OBD-II Real-Time Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/mycarisbroken
ExecStart=/usr/bin/python3 /home/pi/mycarisbroken/obd_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable obd-server.service
sudo systemctl start obd-server.service
sudo systemctl status obd-server.service
```

### Part 2: Mac Setup

#### 1. Find Raspberry Pi IP Address

If you didn't note it from the server startup, SSH into your Pi and run:
```bash
hostname -I
```

#### 2. Access the Dashboard

Open your web browser and navigate to:
```
http://[RASPBERRY_PI_IP]:5000
```

For example:
```
http://192.168.1.150:5000
```

#### 3. Start Monitoring

The dashboard will automatically connect and start monitoring when loaded!

You can also use the control buttons:
- **▶ Start** - Begin OBD data collection
- **⏹ Stop** - Stop monitoring
- **📊 Export CSV** - Download all logged data

## 📊 Available Metrics

The system monitors these OBD-II parameters (if supported by your vehicle):

| Parameter | Description | Unit |
|-----------|-------------|------|
| RPM | Engine RPM | rpm |
| SPEED | Vehicle Speed | km/h |
| ENGINE_LOAD | Calculated Engine Load | % |
| COOLANT_TEMP | Engine Coolant Temperature | °C |
| INTAKE_TEMP | Intake Air Temperature | °C |
| THROTTLE_POS | Throttle Position | % |
| MAF | Mass Air Flow | g/s |
| INTAKE_PRESSURE | Intake Manifold Pressure | kPa |
| FUEL_PRESSURE | Fuel Pressure | kPa |
| TIMING_ADVANCE | Timing Advance | ° |
| FUEL_LEVEL | Fuel Tank Level | % |
| BAROMETRIC_PRESSURE | Barometric Pressure | kPa |
| AMBIANT_AIR_TEMP | Ambient Air Temperature | °C |
| RUN_TIME | Engine Run Time | seconds |

## 🔍 Troubleshooting

### Raspberry Pi Issues

**Server won't start:**
```bash
# Check if port 5000 is already in use
sudo lsof -i :5000

# Check Python version (needs 3.7+)
python3 --version

# Check OBD library installation
python3 -c "import obd; print(obd.__version__)"
```

**Can't connect to OBD adapter:**
```bash
# Check serial ports
ls /dev/tty*

# Check USB devices
lsusb

# Check permissions
sudo chmod 666 /dev/ttyUSB0  # Or your port

# For Bluetooth issues:
sudo systemctl status bluetooth
```

**Import errors:**
```bash
# Reinstall dependencies
pip3 install --upgrade -r requirements_server.txt
```

### Mac/Browser Issues

**Can't access dashboard:**
- Verify Raspberry Pi IP: `ping [RASPBERRY_PI_IP]`
- Check firewall settings on Raspberry Pi
- Try accessing from terminal: `curl http://[RASPBERRY_PI_IP]:5000`
- Verify both devices are on same network

**Dashboard shows "Disconnected":**
- Check if server is running on Raspberry Pi
- Check browser console for errors (F12)
- Try different browser
- Check network connection

**No data appearing:**
- Verify car is running (many OBD commands require engine on)
- Check server logs on Raspberry Pi
- Verify OBD adapter is properly connected
- Some vehicles require specific initialization time

### Common OBD Adapter Issues

**Bluetooth adapter won't connect:**
```bash
# Reset Bluetooth
sudo systemctl restart bluetooth

# Re-pair device
sudo bluetoothctl
remove XX:XX:XX:XX:XX:XX
scan on
pair XX:XX:XX:XX:XX:XX
```

**USB adapter not recognized:**
```bash
# Check kernel messages
dmesg | tail

# Try different USB port
# Check cable quality
```

**"No data" or timeout errors:**
- Increase timeout in code: `obd.Async(fast=False, timeout=30)`
- Try turning car fully on (not just ignition)
- Some cars require drive cycle before full data available

## 📁 Data Storage

All OBD readings are automatically stored in `obd_data.db` (SQLite database).

### Accessing Raw Data

```bash
# On Raspberry Pi
sqlite3 obd_data.db "SELECT * FROM obd_readings LIMIT 10;"

# Export to CSV
sqlite3 -header -csv obd_data.db "SELECT * FROM obd_readings;" > data.csv
```

### Database Schema

```sql
CREATE TABLE obd_readings (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
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
);
```

## 🎨 Customizing the Dashboard

### Modify Update Frequency

Edit `obd_server.py`, line ~190:
```python
time.sleep(0.5)  # Change to 0.1 for faster updates, 1.0 for slower
```

### Add More Metrics

1. Add command to `MONITORED_COMMANDS` list in `obd_server.py`
2. Update database schema in `init_database()`
3. Add metric card to `templates/dashboard.html`

### Change Chart Colors

Edit `templates/dashboard.html`, modify the chart dataset colors:
```javascript
borderColor: 'rgb(255, 99, 132)',  // Chart line color
backgroundColor: 'rgba(255, 99, 132, 0.1)',  // Fill color
```

## 🔐 Security Considerations

**Current setup is for local network use only!**

If exposing to internet:
1. Add authentication (Flask-Login)
2. Use HTTPS (nginx + Let's Encrypt)
3. Implement rate limiting
4. Use strong secret keys
5. Firewall configuration

## 📈 Performance Tips

1. **Network Latency**: Use 5GHz WiFi for better performance
2. **Update Rate**: Balance between data granularity and performance
3. **Chart Data**: Limited to 50 points for smooth rendering
4. **Database**: Regularly export and clear old data

## 🚀 Advanced Usage

### Multiple Simultaneous Clients

The server supports multiple browsers viewing the dashboard simultaneously!

### API Endpoints

Access data programmatically:

```bash
# Connection status
curl http://[RASPBERRY_PI_IP]:5000/api/connection_status

# Supported commands
curl http://[RASPBERRY_PI_IP]:5000/api/supported_commands

# Export CSV
curl http://[RASPBERRY_PI_IP]:5000/api/export_csv > mydata.csv
```

### Python Client

```python
import socketio

sio = socketio.Client()

@sio.on('obd_data')
def on_data(data):
    print(f"RPM: {data.get('RPM')}, Speed: {data.get('SPEED')}")

sio.connect('http://[RASPBERRY_PI_IP]:5000')
sio.wait()
```

## 📚 Understanding the python-OBD Library

This project uses the `python-obd` library. Key concepts:

### Synchronous vs Asynchronous

```python
# Synchronous (one query at a time)
import obd
connection = obd.OBD()
response = connection.query(obd.commands.RPM)
print(response.value)

# Asynchronous (continuous monitoring)
connection = obd.Async()
connection.watch(obd.commands.RPM, callback=lambda r: print(r.value))
connection.start()
```

### Checking Supported Commands

```python
import obd
connection = obd.OBD()

# Check if specific command is supported
if connection.supports(obd.commands.RPM):
    print("RPM is supported")

# List all supported commands
for cmd in connection.supported_commands:
    print(cmd.name, cmd.desc)
```

### Unit Conversions

```python
response = connection.query(obd.commands.SPEED)
print(response.value)  # e.g., 50 kph
print(response.value.to('mph'))  # Convert to mph
```

## 🤝 Contributing

Feel free to fork and improve! Potential enhancements:
- Mobile-responsive improvements
- Additional chart types
- Alert/threshold notifications
- GPS integration
- Drive cycle tracking
- Fuel economy calculations

## 📄 License

GNU GPL v2 (inherited from python-OBD library)

## 🙏 Credits

- **python-OBD**: https://github.com/brendan-w/python-OBD
- **Chart.js**: https://www.chartjs.org/
- **Flask-SocketIO**: https://flask-socketio.readthedocs.io/

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify hardware connections
3. Check server logs on Raspberry Pi
4. Review browser console (F12) for errors

---

**Happy Monitoring! 🚗💨**
