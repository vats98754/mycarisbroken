#!/bin/bash

# WiFi Hotspot Auto-Connect Setup for Raspberry Pi
# This configures your Pi to automatically connect to your phone's hotspot

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     WiFi Hotspot Auto-Connect Setup                     ║"
echo "║     Configure Pi to connect to phone hotspot            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Get hotspot details
echo "Enter your phone's hotspot details:"
echo ""
read -p "Hotspot Name (SSID): " SSID
read -sp "Hotspot Password: " PASSWORD
echo ""
echo ""

# Backup existing config
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.backup

# Add hotspot to wpa_supplicant
echo "Adding hotspot to WiFi configuration..."

sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<EOF

# Phone Hotspot - Auto-connect with highest priority
network={
    ssid="$SSID"
    psk="$PASSWORD"
    priority=100
    id_str="phone_hotspot"
}
EOF

echo "✅ WiFi configuration updated"
echo ""

# Restart WiFi
echo "Restarting WiFi..."
sudo wpa_cli -i wlan0 reconfigure
sleep 3

# Check connection
echo "Checking connection..."
if iwgetid -r; then
    echo "✅ Connected to: $(iwgetid -r)"
    IP=$(hostname -I | awk '{print $1}')
    echo "✅ IP Address: $IP"
    echo ""
    echo "Access dashboard at: http://$IP:5000"
else
    echo "⚠️  Not connected yet. Will auto-connect on next boot."
    echo "   Try rebooting: sudo reboot"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo ""
echo "Your Pi will now automatically connect to this hotspot:"
echo "  SSID: $SSID"
echo ""
echo "This works when:"
echo "  1. You turn on your phone's hotspot"
echo "  2. Your laptop connects to the same hotspot"
echo "  3. Your Raspberry Pi boots up (auto-connects)"
echo "  4. You can access Pi from laptop at http://[PI-IP]:5000"
echo ""
echo "════════════════════════════════════════════════════════════"
