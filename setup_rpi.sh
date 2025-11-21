#!/bin/bash

# Complete Raspberry Pi Setup Script for OBD-II System
# Run this on a fresh Raspberry Pi to install everything needed

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     Raspberry Pi Setup for OBD-II System                ║"
echo "║     Complete Installation from Scratch                  ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Raspberry Pi/Linux
if [[ ! "$OSTYPE" == "linux-gnu"* ]]; then
    echo "⚠️  This script is for Raspberry Pi/Linux only!"
    echo "   Current OS: $OSTYPE"
    exit 1
fi

echo "✓ Detected Linux system"
echo ""

# Update system
echo "════════════════════════════════════════════════════════════"
echo "Step 1: Updating System Packages"
echo "════════════════════════════════════════════════════════════"
echo ""

sudo apt-get update
sudo apt-get upgrade -y

echo ""
echo "✅ System updated"
echo ""

# Install Python and pip
echo "════════════════════════════════════════════════════════════"
echo "Step 2: Installing Python and pip"
echo "════════════════════════════════════════════════════════════"
echo ""

sudo apt-get install -y python3 python3-pip python3-dev

# Verify installation
python3 --version
pip3 --version

echo ""
echo "✅ Python and pip installed"
echo ""

# Install git (if not already installed)
echo "════════════════════════════════════════════════════════════"
echo "Step 3: Installing Git"
echo "════════════════════════════════════════════════════════════"
echo ""

sudo apt-get install -y git

git --version

echo ""
echo "✅ Git installed"
echo ""

# Install system dependencies
echo "════════════════════════════════════════════════════════════"
echo "Step 4: Installing System Dependencies"
echo "════════════════════════════════════════════════════════════"
echo ""

sudo apt-get install -y \
    build-essential \
    python3-setuptools \
    python3-wheel \
    libatlas-base-dev \
    bluetooth \
    bluez

echo ""
echo "✅ System dependencies installed"
echo ""

# Clone or update repository
echo "════════════════════════════════════════════════════════════"
echo "Step 5: Getting OBD-II Code"
echo "════════════════════════════════════════════════════════════"
echo ""

if [ -d "$HOME/mycarisbroken" ]; then
    echo "Directory already exists, pulling latest changes..."
    cd $HOME/mycarisbroken
    git pull
else
    echo "Cloning repository..."
    cd $HOME
    git clone https://github.com/vats98754/mycarisbroken.git
    cd mycarisbroken
fi

echo ""
echo "✅ Code ready in: $HOME/mycarisbroken"
echo ""

# Install Python dependencies
echo "════════════════════════════════════════════════════════════"
echo "Step 6: Installing Python Packages"
echo "════════════════════════════════════════════════════════════"
echo ""

pip3 install --upgrade pip
pip3 install -r requirements_server.txt

echo ""
echo "✅ Python packages installed"
echo ""

# Setup permissions for serial port
echo "════════════════════════════════════════════════════════════"
echo "Step 7: Setting Up Serial Port Permissions"
echo "════════════════════════════════════════════════════════════"
echo ""

# Add user to dialout group for serial access
sudo usermod -a -G dialout $USER

echo "✅ User added to dialout group"
echo "   (You may need to log out and back in for this to take effect)"
echo ""

# Create systemd service (optional)
echo "════════════════════════════════════════════════════════════"
echo "Step 8: Setup Auto-Start Service (Optional)"
echo "════════════════════════════════════════════════════════════"
echo ""

read -p "Would you like the OBD server to start automatically on boot? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating systemd service..."
    
    sudo tee /etc/systemd/system/obd-server.service > /dev/null <<EOF
[Unit]
Description=OBD-II Real-Time Data Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/mycarisbroken
ExecStart=/usr/bin/python3 $HOME/mycarisbroken/obd_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable obd-server.service
    
    echo "✅ Auto-start service created and enabled"
    echo "   Use 'sudo systemctl start obd-server' to start"
    echo "   Use 'sudo systemctl status obd-server' to check status"
else
    echo "⏭  Skipping auto-start service"
fi

echo ""

# Get network information
echo "════════════════════════════════════════════════════════════"
echo "Network Information"
echo "════════════════════════════════════════════════════════════"
echo ""

IP_ADDR=$(hostname -I | awk '{print $1}')
echo "Your Raspberry Pi IP address: $IP_ADDR"
echo ""
echo "Access the dashboard from your Mac at:"
echo "  http://$IP_ADDR:5000"
echo ""

# Final instructions
echo "════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next Steps:"
echo ""
echo "1. Connect your OBD-II adapter:"
echo "   - USB: Plug into Raspberry Pi USB port"
echo "   - Bluetooth: Run 'sudo bluetoothctl' to pair"
echo ""
echo "2. Test the OBD connection:"
echo "   cd $HOME/mycarisbroken"
echo "   python3 test_obd.py"
echo ""
echo "3. Start the server:"
echo "   python3 obd_server.py"
echo ""
echo "4. Open browser on your Mac:"
echo "   http://$IP_ADDR:5000"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📚 Documentation:"
echo "   - START_HERE.md - Quick start guide"
echo "   - QUICKSTART.md - 5-minute setup"
echo "   - REALTIME_SETUP.md - Complete documentation"
echo ""
echo "🔧 Troubleshooting:"
echo "   If you get permission errors, run:"
echo "   sudo chmod 666 /dev/ttyUSB0"
echo ""
echo "   Or logout and login again for group permissions to apply"
echo ""
echo "════════════════════════════════════════════════════════════"
