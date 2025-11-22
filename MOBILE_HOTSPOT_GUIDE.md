# 📱 Mobile Hotspot Setup Guide

## Overview

This setup allows you to:
1. Turn on your phone's hotspot in the car
2. Raspberry Pi automatically connects to it
3. Your laptop connects to the same hotspot
4. Control everything from your laptop remotely

```
┌─────────────────────────────────────────────────┐
│              Your Phone's Hotspot               │
│                (Mobile Data)                    │
└──────────┬─────────────────────┬────────────────┘
           │                     │
    ┌──────▼──────┐      ┌──────▼──────┐
    │ Raspberry Pi│      │Your Laptop  │
    │  (in car)   │      │ (passenger) │
    │             │      │             │
    │ - Auto-     │      │ - Control   │
    │   connects  │      │   Pi via    │
    │ - Runs OBD  │      │   SSH       │
    │   server    │      │ - View      │
    │             │      │   dashboard │
    └─────────────┘      └─────────────┘
```

---

## 🚀 One-Time Setup (On Raspberry Pi)

### Step 1: Run Main Setup

```bash
# SSH into your Pi first time (via home WiFi or ethernet)
ssh pi@raspberrypi.local

# Run complete setup
curl -fsSL https://raw.githubusercontent.com/vats98754/mycarisbroken/master/setup_rpi.sh | bash
```

This will:
- Install Python, pip, git
- Clone the code
- Install dependencies
- Ask if you want to setup WiFi auto-connect

### Step 2: Configure Phone Hotspot

When prompted, enter your phone's hotspot details:
- **SSID**: Your hotspot name
- **Password**: Your hotspot password

The Pi will automatically connect to this hotspot on every boot!

---

## 📱 Daily Usage (In Your Car)

### Every Time You Want to Monitor:

**1. Turn on phone hotspot**
```
Settings → Personal Hotspot → ON
```

**2. Connect laptop to phone hotspot**
```
Same hotspot as Pi is configured for
```

**3. Power on Raspberry Pi**
```
Pi automatically connects to hotspot
Server auto-starts (if configured)
```

**4. From laptop, run remote control**
```bash
cd ~/mycarisbroken  # Or wherever you have the files
./remote_control.sh
```

---

## 🎮 Remote Control Script Usage

The `remote_control.sh` script lets you control your Pi from your laptop:

```bash
./remote_control.sh
```

**Menu Options:**

1. **Test OBD Connection** - Verify adapter is working
2. **Start OBD Server** - Begin data collection
3. **Stop OBD Server** - Stop monitoring
4. **Check Server Status** - See if server is running
5. **View Server Logs** - Debug issues
6. **Open Dashboard** - Launches browser to dashboard
7. **Download Database** - Get all logged data
8. **SSH into Pi** - Full terminal access
9. **Find Pi IP** - Get current IP address
10. **Update Code** - Pull latest changes from GitHub

---

## 💡 Common Workflows

### First Time In Car

```bash
# 1. Check if Pi is reachable
./remote_control.sh
# Choose option 9 (Find Pi IP)

# 2. Test OBD connection
./remote_control.sh
# Choose option 1 (Test OBD)

# 3. Start server
./remote_control.sh
# Choose option 2 (Start Server)

# 4. Open dashboard
./remote_control.sh
# Choose option 6 (Open Dashboard)
```

### Quick Start (After First Time)

```bash
# One command to start and open dashboard
./remote_control.sh
# Choose option 2, answer 'y' to auto-open dashboard
```

### Download Your Data

```bash
./remote_control.sh
# Choose option 7 (Download Database)
# File saved as: obd_data_YYYYMMDD_HHMMSS.db
```

---

## 🔧 Troubleshooting

### Can't Find Raspberry Pi

**Check hotspot:**
```bash
# Make sure phone hotspot is on
# Make sure laptop is connected to hotspot
# Pi should auto-connect within 30 seconds of booting
```

**Try:**
```bash
# On laptop:
ping raspberrypi.local

# Or scan for Pi:
arp -a | grep raspberry
```

### Server Won't Start

**Via remote control:**
```bash
./remote_control.sh
# Choose option 5 (View Logs)
# Look for error messages
```

**Or SSH in:**
```bash
ssh pi@raspberrypi.local
cd ~/mycarisbroken
python3 test_obd.py  # Test OBD first
python3 obd_server.py  # See errors directly
```

### Dashboard Won't Load

**Get Pi IP:**
```bash
./remote_control.sh
# Choose option 9

# Then manually open:
# http://[PI-IP]:5000
```

---

## 🔐 SSH Key Setup (Optional - No Password Needed)

Make SSH faster by setting up keys:

```bash
# On your laptop:
ssh-keygen -t rsa  # Press enter for defaults

# Copy key to Pi:
ssh-copy-id pi@raspberrypi.local

# Now SSH without password!
```

---

## ⚡ Auto-Start Server on Boot

If you want the server to start automatically when Pi boots:

```bash
# During setup, answer 'y' when asked about auto-start

# Or manually:
ssh pi@raspberrypi.local
cd ~/mycarisbroken
sudo cp obd-server.service /etc/systemd/system/
sudo systemctl enable obd-server
sudo systemctl start obd-server
```

---

## 📊 Accessing Dashboard

Once server is running:

**Method 1: Auto-open from remote control**
```bash
./remote_control.sh
# Option 2 or 6
```

**Method 2: Manual**
```bash
# Get Pi IP first
./remote_control.sh  # Option 9

# Then open browser to:
http://192.168.x.x:5000  # Use actual IP
```

**Method 3: Use hostname**
```bash
http://raspberrypi.local:5000
```

---

## 🎯 Complete Example Session

```bash
# Morning: In your car

# 1. Turn on phone hotspot
# 2. Connect laptop to hotspot  
# 3. Turn on Raspberry Pi (in car, plugged into 12V)
# 4. Wait 30 seconds for Pi to boot and connect

# On laptop:
cd ~/mycarisbroken
./remote_control.sh

# Choose: 2 (Start Server)
# Choose: y (Open dashboard)

# Dashboard opens automatically!
# Start driving, watch real-time data

# When done:
./remote_control.sh
# Choose: 3 (Stop Server)
# Choose: 7 (Download Database)

# Turn off Pi, disconnect hotspot
```

---

## 🔄 Updating System

### Update Code on Pi

```bash
./remote_control.sh
# Choose option 10 (Update Code)
```

### Update from Mac

```bash
# Pull latest changes on your Mac
cd ~/mycarisbroken
git pull

# Then update Pi
./remote_control.sh
# Choose option 10
```

---

## 📱 Phone Hotspot Tips

### iPhone
```
Settings → Personal Hotspot
- Turn On
- Note the WiFi Password
- Keep this consistent!
```

### Android
```
Settings → Network & Internet → Hotspot & Tethering
- Turn On
- Configure (set name and password)
- Keep this consistent!
```

**Important:** Use the same hotspot name/password every time so Pi auto-connects!

---

## 🚗 In-Car Power Setup

### Power Raspberry Pi from Car

**Option 1: USB Power**
- Use car USB port or 12V USB adapter
- Needs 5V 2.5A minimum (3A recommended)

**Option 2: Hardwire (Advanced)**
- Connect to always-on 12V circuit
- Use step-down converter to 5V
- Add switch for easy on/off

### Cable Management

- Use velcro to mount Pi to dashboard/console
- Route cables neatly
- Ensure OBD cable can reach port

---

## ✅ Setup Checklist

- [ ] Raspberry Pi setup complete (`setup_rpi.sh`)
- [ ] WiFi auto-connect configured (`setup_wifi.sh`)
- [ ] Auto-start service enabled (optional)
- [ ] Remote control script tested from laptop
- [ ] Phone hotspot name/password saved
- [ ] SSH key setup (optional)
- [ ] Pi mounted in car with power
- [ ] OBD adapter connected
- [ ] Test session completed successfully

---

## 🎓 Next Steps

After everything is working:

1. **Optimize data collection** - Adjust update frequency
2. **Add more sensors** - Monitor additional parameters
3. **Create alerts** - Get notified of issues
4. **Analyze data** - Study your driving patterns
5. **Share dashboard** - Multiple people can view simultaneously

---

**Ready to monitor your car! 🚗💨**
