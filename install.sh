#!/bin/bash

# OBD-II System Installation Helper Script
# This script helps install dependencies on your Raspberry Pi or Mac

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     OBD-II Real-Time Visualization System               ║"
echo "║     Installation Helper                                 ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "✓ Detected: Linux (Raspberry Pi)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo "✓ Detected: macOS"
else
    echo "⚠️  Unknown OS: $OSTYPE"
    OS="unknown"
fi

echo ""
echo "What would you like to install?"
echo ""
echo "  1) Server (for Raspberry Pi - in car)"
echo "  2) Web Dashboard Client (just open browser - no install needed)"
echo "  3) Desktop Client (for Mac - optional)"
echo "  4) Test utilities only"
echo "  5) Everything"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "📦 Installing OBD Server dependencies..."
        echo ""
        
        if [ "$OS" = "linux" ]; then
            echo "Installing system packages..."
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-dev
        fi
        
        echo "Installing Python packages..."
        pip3 install -r requirements_server.txt
        
        echo ""
        echo "✅ Server installation complete!"
        echo ""
        echo "Next steps:"
        echo "  1. Connect your OBD-II adapter"
        echo "  2. Test with: python3 test_obd.py"
        echo "  3. Run server: python3 obd_server.py"
        ;;
        
    2)
        echo ""
        echo "ℹ️  Web Dashboard Client"
        echo ""
        echo "No installation needed! The dashboard is served by the server."
        echo ""
        echo "To access:"
        echo "  1. Make sure obd_server.py is running on Raspberry Pi"
        echo "  2. Note the IP address shown when server starts"
        echo "  3. Open browser on your Mac"
        echo "  4. Navigate to: http://[RASPBERRY_PI_IP]:5000"
        echo ""
        echo "Example: http://192.168.1.150:5000"
        ;;
        
    3)
        echo ""
        echo "📦 Installing Desktop Client dependencies..."
        echo ""
        
        if [ "$OS" = "mac" ]; then
            # Check if Homebrew is installed
            if ! command -v brew &> /dev/null; then
                echo "⚠️  Homebrew not found. Install from: https://brew.sh"
                exit 1
            fi
            
            echo "Installing Python via Homebrew..."
            brew install python-tk
        fi
        
        echo "Installing Python packages..."
        pip3 install -r requirements_mac.txt
        
        echo ""
        echo "✅ Desktop client installation complete!"
        echo ""
        echo "To run: python3 mac_client.py"
        ;;
        
    4)
        echo ""
        echo "📦 Installing test utilities..."
        echo ""
        
        # Just install basic obd library
        pip3 install obd
        
        echo ""
        echo "✅ Test utilities ready!"
        echo ""
        echo "To test: python3 test_obd.py"
        ;;
        
    5)
        echo ""
        echo "📦 Installing everything..."
        echo ""
        
        if [ "$OS" = "linux" ]; then
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-dev
        fi
        
        pip3 install -r requirements_server.txt
        pip3 install -r requirements_mac.txt
        
        echo ""
        echo "✅ Complete installation finished!"
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📚 Documentation:"
echo "   - QUICKSTART.md - 5 minute setup guide"
echo "   - REALTIME_SETUP.md - Complete documentation"
echo "   - PROJECT_SUMMARY.md - System overview"
echo ""
echo "🧪 Test first:"
echo "   python3 test_obd.py"
echo ""
echo "🚀 Then run:"
echo "   python3 obd_server.py"
echo "════════════════════════════════════════════════════════════"
