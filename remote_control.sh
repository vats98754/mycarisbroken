#!/bin/bash

# Remote Control Script - Run from your Laptop
# This lets you control the Raspberry Pi OBD server from your laptop

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     OBD Server Remote Control                           ║"
echo "║     Control Raspberry Pi from your Laptop               ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Get Pi IP address or hostname
read -p "Enter Raspberry Pi IP or hostname [raspberrypi.local]: " PI_HOST
PI_HOST=${PI_HOST:-raspberrypi.local}

echo ""
echo "What would you like to do?"
echo ""
echo "  1) Test OBD Connection (run test_obd.py)"
echo "  2) Start OBD Server (run obd_server.py)"
echo "  3) Stop OBD Server"
echo "  4) Check Server Status"
echo "  5) View Server Logs"
echo "  6) Open Dashboard in Browser"
echo "  7) Download Database (obd_data.db)"
echo "  8) SSH into Raspberry Pi"
echo "  9) Find Raspberry Pi IP Address"
echo "  10) Update Code on Pi"
echo ""
read -p "Enter choice [1-10]: " choice

case $choice in
    1)
        echo ""
        echo "🧪 Running OBD Connection Test on Raspberry Pi..."
        echo "════════════════════════════════════════════════════════════"
        ssh pi@$PI_HOST "cd ~/mycarisbroken && python3 test_obd.py"
        ;;
        
    2)
        echo ""
        echo "🚀 Starting OBD Server on Raspberry Pi..."
        echo "════════════════════════════════════════════════════════════"
        echo ""
        echo "Starting server in background..."
        ssh pi@$PI_HOST "cd ~/mycarisbroken && nohup python3 obd_server.py > obd_server.log 2>&1 &"
        sleep 2
        
        echo ""
        echo "✅ Server started!"
        echo ""
        echo "Getting Pi IP address..."
        PI_IP=$(ssh pi@$PI_HOST "hostname -I | awk '{print \$1}'")
        echo "✅ Pi IP: $PI_IP"
        echo ""
        echo "Open dashboard in browser:"
        echo "  http://$PI_IP:5000"
        echo ""
        read -p "Open dashboard now? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "http://$PI_IP:5000" 2>/dev/null || xdg-open "http://$PI_IP:5000" 2>/dev/null || echo "Open manually: http://$PI_IP:5000"
        fi
        ;;
        
    3)
        echo ""
        echo "⏹  Stopping OBD Server on Raspberry Pi..."
        echo "════════════════════════════════════════════════════════════"
        ssh pi@$PI_HOST "pkill -f obd_server.py"
        echo "✅ Server stopped"
        ;;
        
    4)
        echo ""
        echo "📊 Checking Server Status..."
        echo "════════════════════════════════════════════════════════════"
        if ssh pi@$PI_HOST "pgrep -f obd_server.py > /dev/null"; then
            echo "✅ Server is RUNNING"
            PI_IP=$(ssh pi@$PI_HOST "hostname -I | awk '{print \$1}'")
            echo "   Access at: http://$PI_IP:5000"
        else
            echo "❌ Server is NOT running"
        fi
        ;;
        
    5)
        echo ""
        echo "📜 Server Logs..."
        echo "════════════════════════════════════════════════════════════"
        ssh pi@$PI_HOST "cd ~/mycarisbroken && tail -50 obd_server.log"
        ;;
        
    6)
        echo ""
        echo "🌐 Opening Dashboard..."
        echo "════════════════════════════════════════════════════════════"
        PI_IP=$(ssh pi@$PI_HOST "hostname -I | awk '{print \$1}'")
        echo "Pi IP: $PI_IP"
        open "http://$PI_IP:5000" 2>/dev/null || xdg-open "http://$PI_IP:5000" 2>/dev/null || echo "Open manually: http://$PI_IP:5000"
        ;;
        
    7)
        echo ""
        echo "📥 Downloading Database..."
        echo "════════════════════════════════════════════════════════════"
        scp pi@$PI_HOST:~/mycarisbroken/obd_data.db ./obd_data_$(date +%Y%m%d_%H%M%S).db
        echo "✅ Database downloaded to current directory"
        ;;
        
    8)
        echo ""
        echo "🔐 Opening SSH Session..."
        echo "════════════════════════════════════════════════════════════"
        ssh pi@$PI_HOST
        ;;
        
    9)
        echo ""
        echo "🔍 Finding Raspberry Pi..."
        echo "════════════════════════════════════════════════════════════"
        echo ""
        echo "Method 1: Using hostname"
        ping -c 1 raspberrypi.local 2>/dev/null | grep "bytes from" | awk '{print $4}' | sed 's/:$//'
        echo ""
        echo "Method 2: Getting IP from Pi"
        PI_IP=$(ssh pi@$PI_HOST "hostname -I | awk '{print \$1}'" 2>/dev/null)
        if [ ! -z "$PI_IP" ]; then
            echo "Raspberry Pi IP: $PI_IP"
            echo ""
            echo "Access dashboard at: http://$PI_IP:5000"
        else
            echo "Could not connect to Pi"
            echo ""
            echo "Make sure:"
            echo "  - Your phone's hotspot is on"
            echo "  - Your laptop is connected to the hotspot"
            echo "  - Raspberry Pi is powered on and connected"
        fi
        ;;
        
    10)
        echo ""
        echo "🔄 Updating Code on Raspberry Pi..."
        echo "════════════════════════════════════════════════════════════"
        ssh pi@$PI_HOST "cd ~/mycarisbroken && git pull"
        echo "✅ Code updated"
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════"
