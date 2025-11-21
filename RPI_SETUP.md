# 🔧 Raspberry Pi Setup from Scratch

## One-Command Setup

```bash
curl -fsSL https://raw.githubusercontent.com/vats98754/mycarisbroken/master/setup_rpi.sh | bash
```

**OR** if you have the files already:

```bash
chmod +x setup_rpi.sh
./setup_rpi.sh
```

---

## Manual Setup (If Script Doesn't Work)

### 1. Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install Python and pip

```bash
sudo apt-get install -y python3 python3-pip python3-dev
```

### 3. Install Git

```bash
sudo apt-get install -y git
```

### 4. Get the Code

```bash
cd ~
git clone https://github.com/vats98754/mycarisbroken.git
cd mycarisbroken
```

### 5. Install Dependencies

```bash
pip3 install -r requirements_server.txt
```

### 6. Fix Permissions

```bash
sudo usermod -a -G dialout $USER
```

Then **logout and login again**.

### 7. Test OBD Connection

```bash
python3 test_obd.py
```

### 8. Start Server

```bash
python3 obd_server.py
```

---

## Quick Transfer from Mac

If you want to copy files from your Mac to Raspberry Pi:

```bash
# On your Mac:
scp -r /Users/anvayvats/mycarisbroken pi@raspberrypi.local:~/

# Then SSH into Pi:
ssh pi@raspberrypi.local

# Run setup:
cd mycarisbroken
chmod +x setup_rpi.sh
./setup_rpi.sh
```

---

## Finding Your Pi's IP

```bash
hostname -I
```

Use this IP to access dashboard: `http://[IP]:5000`
