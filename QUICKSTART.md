# 🚀 Quick Start Guide - OBD-II Real-Time Visualization

## TL;DR - Get Running in 5 Minutes

### On Raspberry Pi (in your car)

```bash
# 1. Install dependencies
pip3 install -r requirements_server.txt

# 2. Plug in your OBD-II adapter (USB or Bluetooth)

# 3. Start the server
python3 obd_server.py

# 4. Note the IP address shown (e.g., 192.168.1.150)
```

### On Your Mac (anywhere on same network)

**Option 1: Web Browser (Recommended)**

```
Open browser → http://[RASPBERRY_PI_IP]:5000
```

**Option 2: Desktop App**

```bash
# Install dependencies
pip3 install -r requirements_mac.txt

# Run the app
python3 mac_client.py
```

---

## What This System Does

```
┌─────────────────┐     WiFi/Network     ┌──────────────┐
│  Raspberry Pi   │ ═══════════════════► │  Your Mac    │
│  (in car)       │                       │  (anywhere)  │
│                 │                       │              │
│  ┌──────────┐   │                       │ ┌──────────┐ │
│  │ OBD-II   │   │                       │ │ Dashboard│ │
│  │ Adapter  │   │                       │ │ Charts   │ │
│  └────┬─────┘   │                       │ │ Metrics  │ │
│       │         │                       │ └──────────┘ │
│  ┌────▼─────┐   │                       │              │
│  │ Your Car │   │                       │              │
│  │ ECU      │   │                       │              │
│  └──────────┘   │                       │              │
└─────────────────┘                       └──────────────┘
```

**The Raspberry Pi:**
- Connects to your car's OBD-II port
- Reads real-time sensor data (RPM, speed, temperature, etc.)
- Broadcasts data over your network
- Stores all data in SQLite database

**Your Mac:**
- Displays beautiful real-time charts
- Shows current sensor values
- Can export data to CSV
- Works from anywhere on same network

---

## Understanding the Components

### 1. Python OBD Library (`obd`)

This library talks to your car through the ELM327 adapter.

**Key Concepts:**

```python
import obd

# Connect to car
connection = obd.OBD()  # Auto-finds adapter

# Query a sensor
response = connection.query(obd.commands.RPM)
print(response.value)  # e.g., 2500 rpm

# Check what's supported
if connection.supports(obd.commands.SPEED):
    speed = connection.query(obd.commands.SPEED)
```

**Async Mode (What We Use):**

```python
connection = obd.Async()  # Async mode

# Watch multiple sensors continuously
connection.watch(obd.commands.RPM)
connection.watch(obd.commands.SPEED)

connection.start()  # Start monitoring

# Query anytime - gets latest value
rpm = connection.query(obd.commands.RPM)
```

### 2. Server (`obd_server.py`)

**What it does:**
1. Connects to OBD adapter
2. Monitors 14+ sensors continuously
3. Broadcasts data via WebSocket to all connected clients
4. Stores everything in SQLite database

**Key functions:**
- `connect_obd()` - Establishes OBD connection
- `collect_data()` - Main loop that reads sensors
- `store_reading()` - Saves to database
- WebSocket events for real-time streaming

### 3. Dashboard (`templates/dashboard.html`)

**Features:**
- Real-time metrics display (big numbers)
- 4 live-updating charts
- Auto-connects and starts monitoring
- Export to CSV button

**Technologies:**
- Socket.IO - Real-time WebSocket communication
- Chart.js - Beautiful animated charts
- Vanilla JavaScript - No framework needed

---

## Common Scenarios

### Scenario 1: Monitor While Driving

```bash
# In car (Raspberry Pi):
python3 obd_server.py

# On Mac (passenger or later):
Open http://[PI_IP]:5000
```

Data is automatically logged. Review charts in real-time or export later.

### Scenario 2: Diagnose an Issue

```bash
# Start monitoring
# Drive normally / reproduce issue
# Click "Export CSV"
# Analyze data in Excel/Python
```

### Scenario 3: Multiple People Watching

```bash
# One Raspberry Pi in car
# Multiple browsers can connect:
# - Driver's phone
# - Passenger's laptop  
# - Remote laptop (if same network)
```

All see the same real-time data!

---

## Data You Can Monitor

| Metric | What It Tells You | Normal Range |
|--------|-------------------|--------------|
| **RPM** | Engine speed | 700-800 idle, 2000-3000 cruising |
| **SPEED** | Vehicle speed | As expected |
| **ENGINE_LOAD** | How hard engine is working | 20-30% cruising, 80%+ accelerating |
| **COOLANT_TEMP** | Engine temperature | 85-105°C normal operating |
| **INTAKE_TEMP** | Air intake temperature | Near ambient when cold |
| **THROTTLE_POS** | Accelerator position | 0% idle, 100% floored |
| **MAF** | Air flow into engine | Higher = more power |
| **INTAKE_PRESSURE** | Manifold pressure | Related to throttle |
| **FUEL_PRESSURE** | Fuel system pressure | Vehicle specific |
| **TIMING_ADVANCE** | Ignition timing | Varies with load/RPM |

---

## Troubleshooting One-Pagers

### "Can't connect to OBD adapter"

```bash
# Check if adapter is detected
ls /dev/tty*

# For USB: Look for /dev/ttyUSB0
# For Bluetooth: Look for /dev/rfcomm0

# Fix permissions
sudo chmod 666 /dev/ttyUSB0

# Test connection
python3 -c "import obd; print(obd.scan_serial())"
```

### "Dashboard won't load"

```bash
# On Mac, check if server is reachable
ping [RASPBERRY_PI_IP]

# Should reply with times

# Check if port 5000 is open
curl http://[RASPBERRY_PI_IP]:5000

# Should return HTML
```

### "Connected but no data"

**Most common cause:** Car engine is off

```
1. Turn car to "ON" position (or start engine)
2. Wait 10 seconds for ECU to initialize
3. Data should start flowing
```

**Other causes:**
- Adapter not fully connected to OBD port
- Adapter not compatible with vehicle
- Vehicle requires specific protocol

### "Bluetooth adapter won't connect"

```bash
# Pair first
sudo bluetoothctl
scan on
# Wait for device
pair AA:BB:CC:DD:EE:FF
connect AA:BB:CC:DD:EE:FF
exit

# Create serial port
sudo rfcomm bind /dev/rfcomm0 AA:BB:CC:DD:EE:FF
```

---

## Advanced Tips

### Find Your Raspberry Pi on Network

```bash
# On Mac:
ping raspberrypi.local

# Or scan network:
arp -a | grep raspberry

# On Pi itself:
hostname -I
```

### Change Update Frequency

Edit `obd_server.py`, line ~190:

```python
time.sleep(0.5)  # Default: 2 updates/second

# Faster (might overwhelm some adapters):
time.sleep(0.1)  # 10 updates/second

# Slower (saves bandwidth):
time.sleep(1.0)  # 1 update/second
```

### Access from Different Network

```bash
# On Raspberry Pi:
# Install ngrok or use VPN

# Quick ngrok method:
./ngrok http 5000

# Use provided URL on any device
```

### Export and Analyze Data

```python
import pandas as pd
import sqlite3

# Read database
conn = sqlite3.connect('obd_data.db')
df = pd.read_sql_query("SELECT * FROM obd_readings", conn)

# Analyze
print(df.describe())
print(f"Max RPM: {df['rpm'].max()}")
print(f"Avg Speed: {df['speed'].mean()}")

# Plot
import matplotlib.pyplot as plt
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.plot(x='timestamp', y=['rpm', 'speed'])
plt.show()
```

---

## File Structure Explained

```
mycarisbroken/
├── obd_server.py          # Main server (run on Raspberry Pi)
├── mac_client.py          # Optional desktop client (run on Mac)
├── templates/
│   └── dashboard.html     # Web dashboard (auto-served by server)
├── requirements_server.txt # Install on Raspberry Pi
├── requirements_mac.txt   # Install on Mac (optional)
├── REALTIME_SETUP.md      # Full documentation
├── QUICKSTART.md          # This file
└── obd/                   # python-obd library (already here)
```

---

## Next Steps

1. **Test locally first**
   - Connect adapter to laptop
   - Run server
   - Access dashboard on localhost:5000

2. **Deploy to Raspberry Pi**
   - Copy files to Pi
   - Set up in car
   - Connect from Mac

3. **Customize**
   - Add more metrics
   - Adjust chart colors
   - Create alerts for thresholds

---

## Resources

- **python-OBD Docs**: http://python-obd.readthedocs.org/
- **OBD-II PIDs**: https://en.wikipedia.org/wiki/OBD-II_PIDs
- **ELM327 Datasheet**: https://www.elmelectronics.com/

---

## One-Line Summaries

**For complete beginners:**
> This lets you see what your car is doing in real-time on your Mac, like RPM and speed, by plugging a $20 adapter into your car and using a Raspberry Pi.

**For developers:**
> Flask-SocketIO server on Pi streams OBD-II data from python-obd library to Chart.js dashboard via WebSocket with SQLite logging.

**For car enthusiasts:**
> Real-time OBD-II scanner with data logging, graphing, and remote viewing - like a professional scan tool but better.

---

**Questions? Check REALTIME_SETUP.md for detailed documentation!**
