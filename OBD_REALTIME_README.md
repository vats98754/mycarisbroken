# 🚗 OBD-II Real-Time Visualization System

**Stream live vehicle data from your Raspberry Pi to your Mac over WiFi**

![System Overview](https://img.shields.io/badge/Raspberry_Pi-Ready-red?logo=raspberry-pi)
![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)
![License](https://img.shields.io/badge/License-GPL_v2-green)

---

## 🎯 What Is This?

A complete system for **real-time vehicle diagnostics** that:

- 📊 **Monitors** your car's OBD-II sensors in real-time
- 📡 **Streams** data wirelessly from Raspberry Pi to your Mac
- 📈 **Visualizes** data with beautiful, live-updating charts
- 💾 **Logs** everything to SQLite database
- 📤 **Exports** data to CSV for analysis

**Perfect for:** Performance monitoring, diagnostics, learning how your car works, track days, fuel economy analysis

---

## ⚡ Quick Start

### 1️⃣ On Raspberry Pi (in car)

```bash
./install.sh          # Run installer
python3 test_obd.py   # Test OBD connection
python3 obd_server.py # Start streaming
```

### 2️⃣ On Your Mac (anywhere on network)

```
Open browser → http://192.168.1.XXX:5000
```

**That's it!** Real-time charts appear automatically.

---

## 📁 What's Included

```
mycarisbroken/
├── 🚀 QUICKSTART.md          # Start here! 5-min setup
├── 📖 REALTIME_SETUP.md      # Complete documentation
├── 📋 PROJECT_SUMMARY.md     # System overview
│
├── 🔧 install.sh             # Installation helper
├── 🧪 test_obd.py            # Test your OBD adapter
│
├── 🖥️  obd_server.py          # Main server (Raspberry Pi)
├── 🌐 templates/
│   └── dashboard.html        # Web dashboard
│
├── 🖼️  mac_client.py          # Optional desktop app
│
├── 📦 requirements_server.txt # Pi dependencies
├── 📦 requirements_mac.txt    # Mac dependencies
│
└── 🔌 obd/                    # python-obd library (included)
```

---

## 🎬 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR VEHICLE                        │
│  ┌──────────┐                                           │
│  │   ECU    │ ◄─── Reads real-time sensor data         │
│  └────┬─────┘                                           │
│       │                                                 │
│  ┌────▼────────┐                                        │
│  │  OBD-II Port│ ◄─── Standard diagnostic port         │
│  └────┬────────┘                                        │
└───────┼─────────────────────────────────────────────────┘
        │
   ┌────▼────────┐
   │ ELM327      │ ◄─── USB/Bluetooth adapter ($20)
   │ Adapter     │
   └────┬────────┘
        │
┌───────▼──────────────────────────────────────────────────┐
│              RASPBERRY PI (in car)                       │
│                                                          │
│  ┌────────────────────────────────────┐                 │
│  │  obd_server.py                     │                 │
│  │  ├─ python-obd library             │                 │
│  │  ├─ Flask web server                │                 │
│  │  ├─ Socket.IO (WebSocket)          │                 │
│  │  └─ SQLite database                │                 │
│  └────────────────────────────────────┘                 │
│                                                          │
└────────────┬─────────────────────────────────────────────┘
             │
             │ WiFi/Network (WebSocket streaming)
             │
┌────────────▼─────────────────────────────────────────────┐
│              YOUR MAC (anywhere on network)              │
│                                                          │
│  ┌────────────────────────────────────┐                 │
│  │  Web Browser Dashboard             │                 │
│  │  ├─ Real-time charts (Chart.js)    │                 │
│  │  ├─ Live metrics display           │                 │
│  │  ├─ CSV export                     │                 │
│  │  └─ Auto-updating (2 Hz)           │                 │
│  └────────────────────────────────────┘                 │
│                                                          │
│         OR (optional)                                    │
│                                                          │
│  ┌────────────────────────────────────┐                 │
│  │  Desktop Client (mac_client.py)    │                 │
│  │  └─ Matplotlib charts              │                 │
│  └────────────────────────────────────┘                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 Monitored Parameters

| **Metric** | **Description** | **Unit** |
|-----------|----------------|---------|
| RPM | Engine speed | rpm |
| SPEED | Vehicle speed | km/h |
| ENGINE_LOAD | Calculated engine load | % |
| COOLANT_TEMP | Engine coolant temperature | °C |
| INTAKE_TEMP | Intake air temperature | °C |
| THROTTLE_POS | Throttle position | % |
| MAF | Mass air flow | g/s |
| INTAKE_PRESSURE | Intake manifold pressure | kPa |
| FUEL_PRESSURE | Fuel rail pressure | kPa |
| TIMING_ADVANCE | Ignition timing | ° |
| FUEL_LEVEL | Fuel tank level | % |
| BAROMETRIC_PRESSURE | Atmospheric pressure | kPa |
| AMBIANT_AIR_TEMP | Ambient temperature | °C |
| RUN_TIME | Engine run time | seconds |

*Actual metrics depend on your vehicle's OBD-II support*

---

## 🛠️ Installation

### Option 1: Automated Install

```bash
chmod +x install.sh
./install.sh
# Follow the prompts
```

### Option 2: Manual Install

**On Raspberry Pi:**
```bash
pip3 install -r requirements_server.txt
```

**On Mac (for desktop client - optional):**
```bash
pip3 install -r requirements_mac.txt
```

---

## 🚀 Usage

### Basic Workflow

```bash
# 1. Test hardware connection
python3 test_obd.py

# 2. Start server (on Raspberry Pi)
python3 obd_server.py

# 3. Access dashboard (on Mac browser)
http://[RASPBERRY_PI_IP]:5000

# 4. Data is automatically logged
# 5. Export anytime via "Export CSV" button
```

### Finding Your Raspberry Pi IP

**On Raspberry Pi:**
```bash
hostname -I
```

**On Mac:**
```bash
ping raspberrypi.local
```

---

## 📸 Screenshots

### Web Dashboard
- **Big Metrics**: Real-time RPM, Speed, Temperature, Load
- **Live Charts**: 4 animated graphs with 50-point history
- **Controls**: Start/Stop monitoring, Export data
- **Status**: Connection indicator, error messages

### Desktop Client
- **Native App**: Tkinter-based GUI
- **Matplotlib Charts**: Professional plotting
- **Connection Manager**: Easy server configuration

---

## 🎓 Understanding the Code

### python-obd Library

**Core concept:**
```python
import obd

# Connect to adapter
connection = obd.Async()

# Watch sensors
connection.watch(obd.commands.RPM)
connection.watch(obd.commands.SPEED)

# Start monitoring
connection.start()

# Query anytime
rpm = connection.query(obd.commands.RPM)
print(rpm.value)  # e.g., 2500 rpm
```

### Server Architecture

1. **OBD Layer**: python-obd connects to ELM327 adapter
2. **Data Collection**: Async loop queries sensors every 0.5s
3. **Storage**: SQLite database logs all readings
4. **Broadcasting**: Socket.IO sends data to all connected clients
5. **Web Serving**: Flask serves dashboard HTML

### Client Architecture

1. **Socket.IO Client**: Connects to server via WebSocket
2. **Event Handlers**: Receives `obd_data` events
3. **Chart.js**: Renders animated line charts
4. **DOM Updates**: Updates metric displays in real-time

---

## 🔧 Customization

### Change Update Frequency

Edit `obd_server.py` line ~190:
```python
time.sleep(0.5)  # Change this value
# 0.1 = 10 Hz (fast)
# 0.5 = 2 Hz (default)
# 1.0 = 1 Hz (slow)
```

### Add More Sensors

1. **Find command** in `obd/commands.py`
2. **Add to list** in `obd_server.py`:
   ```python
   MONITORED_COMMANDS = [
       # ... existing ...
       ('NEW_SENSOR', obd.commands.NEW_SENSOR),
   ]
   ```
3. **Update database** schema
4. **Add to dashboard** HTML

### Modify Dashboard Design

Edit `templates/dashboard.html`:
- Colors: Search for `rgb()` values
- Layout: Modify CSS grid
- Charts: Change Chart.js options

---

## 🐛 Troubleshooting

### Common Issues

| **Problem** | **Solution** |
|------------|------------|
| No OBD adapter found | Check USB/Bluetooth connection |
| Permission denied | `sudo chmod 666 /dev/ttyUSB0` |
| Can't connect to car | Turn car ON, wait 10 seconds |
| Dashboard won't load | Verify IP with `ping` |
| No data in charts | Engine must be running |
| Import errors | Re-run `pip3 install -r requirements_server.txt` |

### Detailed Troubleshooting

See **REALTIME_SETUP.md** section "Troubleshooting" for:
- Bluetooth pairing issues
- Protocol detection problems
- Network configuration
- Database access errors

---

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[REALTIME_SETUP.md](REALTIME_SETUP.md)** - Complete setup guide (350+ lines)
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical overview

---

## 🎯 Use Cases

### 1. **Real-Time Monitoring**
Monitor engine parameters while driving. Great for:
- Performance driving
- Diagnosing issues
- Learning engine behavior

### 2. **Data Logging**
Record all sensor data for later analysis:
- Track day analysis
- Fuel economy studies
- Emissions testing
- Long-term trends

### 3. **Diagnostics**
Identify problems by watching sensor patterns:
- Check engine light investigation
- Temperature issues
- Fuel system problems
- Air/fuel ratio analysis

### 4. **Education**
Learn how cars work:
- See throttle vs RPM relationship
- Watch coolant temp during warmup
- Understand engine load
- Observe timing advance

---

## 🔐 Security Notes

**Current setup is for LOCAL NETWORK use only.**

If exposing to internet:
- Add authentication (Flask-Login)
- Use HTTPS (nginx + Let's Encrypt)
- Implement rate limiting
- Use environment variables for secrets
- Configure firewall properly

---

## 🌟 Advanced Features

### Multiple Clients
Multiple browsers/devices can view simultaneously!

### API Endpoints
```bash
# Connection status
curl http://[PI_IP]:5000/api/connection_status

# Supported commands
curl http://[PI_IP]:5000/api/supported_commands

# Export CSV
curl http://[PI_IP]:5000/api/export_csv > data.csv
```

### Python Client
```python
import socketio

sio = socketio.Client()

@sio.on('obd_data')
def on_data(data):
    print(f"RPM: {data['RPM']}")

sio.connect('http://[PI_IP]:5000')
sio.wait()
```

---

## 📦 Dependencies

### Server (Raspberry Pi)
- Python 3.7+
- flask
- flask-socketio
- flask-cors
- python-socketio
- eventlet
- obd (python-obd)

### Client (Mac - optional)
- python-socketio[client]
- matplotlib

---

## 🤝 Contributing

Ideas for enhancements:
- [ ] GPS integration
- [ ] Fuel economy calculator
- [ ] Alert system (high temp, etc.)
- [ ] Mobile app
- [ ] Cloud sync
- [ ] Machine learning predictions
- [ ] Drive cycle tracking

---

## 📄 License

GNU GPL v2 (inherited from python-OBD)

See [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- **python-OBD** by Brendan Whitfield
- **Chart.js** by Chart.js community
- **Flask-SocketIO** by Miguel Grinberg
- **ELM327** protocol by ELM Electronics

---

## 📞 Support

1. Check **QUICKSTART.md** for common issues
2. Run `python3 test_obd.py` to verify hardware
3. Review server logs for error messages
4. Check browser console (F12) for client errors

---

## 🎉 Get Started Now!

```bash
# 1. Install
./install.sh

# 2. Test
python3 test_obd.py

# 3. Run
python3 obd_server.py

# 4. Open browser
http://[your-pi-ip]:5000
```

**Enjoy real-time car data! 🚗💨**

---

*Built with ❤️ for car enthusiasts and makers*
