#!/usr/bin/env python3
"""
OBD Connection Test Script
Use this to verify your OBD adapter is working before running the full server
"""

import obd
import time
import sys


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def test_connection():
    """Test basic OBD connection"""
    print_header("1. Testing OBD Connection")
    
    print("\n🔍 Scanning for OBD adapters...")
    ports = obd.scan_serial()
    
    if not ports:
        print("❌ No OBD adapters found!")
        print("\nTroubleshooting:")
        print("  - Check if adapter is plugged in")
        print("  - For USB: Run 'ls /dev/ttyUSB*'")
        print("  - For Bluetooth: Ensure device is paired and rfcomm is bound")
        return None
    
    print(f"✅ Found {len(ports)} port(s):")
    for port in ports:
        print(f"   - {port}")
    
    print("\n🔌 Connecting to OBD adapter...")
    connection = obd.OBD(fast=False, timeout=30)
    
    if connection.is_connected():
        print("✅ Successfully connected!")
        print(f"   Protocol: {connection.protocol_name()}")
        print(f"   Port: {connection.port_name()}")
        return connection
    else:
        print("❌ Failed to connect")
        print("\nMake sure:")
        print("  - Car is in ON position or engine is running")
        print("  - Adapter is fully inserted into OBD port")
        print("  - You have proper permissions (try: sudo)")
        return None


def test_supported_commands(connection):
    """Check which commands are supported"""
    print_header("2. Checking Supported Commands")
    
    if not connection:
        return
    
    supported = connection.supported_commands
    print(f"\n✅ Your vehicle supports {len(supported)} commands")
    
    # Show some important ones
    important_commands = [
        obd.commands.RPM,
        obd.commands.SPEED,
        obd.commands.ENGINE_LOAD,
        obd.commands.COOLANT_TEMP,
        obd.commands.THROTTLE_POS,
        obd.commands.INTAKE_PRESSURE,
        obd.commands.MAF,
        obd.commands.FUEL_LEVEL,
    ]
    
    print("\nChecking key commands:")
    for cmd in important_commands:
        if connection.supports(cmd):
            print(f"   ✅ {cmd.name} - {cmd.desc}")
        else:
            print(f"   ❌ {cmd.name} - Not supported")


def test_live_data(connection):
    """Test reading live data"""
    print_header("3. Testing Live Data Readings")
    
    if not connection:
        return
    
    print("\n📊 Reading live data (10 samples)...")
    print("   (If all values are None, make sure engine is running)\n")
    
    commands_to_test = [
        obd.commands.RPM,
        obd.commands.SPEED,
        obd.commands.ENGINE_LOAD,
        obd.commands.COOLANT_TEMP,
    ]
    
    for i in range(10):
        print(f"Sample {i+1}/10:")
        for cmd in commands_to_test:
            if connection.supports(cmd):
                response = connection.query(cmd)
                if not response.is_null():
                    # Extract the numeric value
                    if hasattr(response.value, 'magnitude'):
                        value = f"{response.value.magnitude:.1f} {response.value.units}"
                    else:
                        value = str(response.value)
                    print(f"   {cmd.name:20} = {value}")
                else:
                    print(f"   {cmd.name:20} = No data")
        print()
        time.sleep(1)


def test_async_mode(connection):
    """Test async mode (what the server uses)"""
    print_header("4. Testing Async Mode")
    
    print("\n⚙️ Creating async connection...")
    async_conn = obd.Async(fast=False, timeout=30)
    
    if not async_conn.is_connected():
        print("❌ Failed to create async connection")
        return
    
    print("✅ Async connection created")
    
    # Watch some commands
    print("\n👀 Watching RPM and SPEED...")
    if async_conn.supports(obd.commands.RPM):
        async_conn.watch(obd.commands.RPM)
    if async_conn.supports(obd.commands.SPEED):
        async_conn.watch(obd.commands.SPEED)
    
    print("▶️ Starting async loop...")
    async_conn.start()
    
    print("\n📊 Reading async data (5 samples):")
    for i in range(5):
        time.sleep(1)
        rpm_response = async_conn.query(obd.commands.RPM)
        speed_response = async_conn.query(obd.commands.SPEED)
        
        rpm = "N/A"
        speed = "N/A"
        
        if not rpm_response.is_null() and hasattr(rpm_response.value, 'magnitude'):
            rpm = f"{rpm_response.value.magnitude:.0f}"
        
        if not speed_response.is_null() and hasattr(speed_response.value, 'magnitude'):
            speed = f"{speed_response.value.magnitude:.0f}"
        
        print(f"   Sample {i+1}: RPM={rpm}, SPEED={speed}")
    
    print("\n⏹ Stopping async loop...")
    async_conn.stop()
    async_conn.close()
    print("✅ Async test complete")


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          OBD-II Connection Test Script                  ║
║                                                          ║
║  This will verify your OBD adapter is working           ║
║  before running the full visualization server           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    print("⚠️ IMPORTANT:")
    print("   - Make sure your car is in ON position (or engine running)")
    print("   - OBD adapter should be plugged into the OBD-II port")
    print("   - Wait a few seconds after turning on the car")
    
    input("\n👉 Press ENTER when ready to start testing...")
    
    # Test connection
    connection = test_connection()
    
    if connection:
        # Test supported commands
        test_supported_commands(connection)
        
        # Test live data
        test_live_data(connection)
        
        # Close synchronous connection
        connection.close()
        
        # Test async mode
        test_async_mode(connection)
        
        print_header("✅ All Tests Complete!")
        print("\n✨ Your OBD adapter is working correctly!")
        print("\n🚀 You can now run the full server:")
        print("   python3 obd_server.py")
        
    else:
        print_header("❌ Tests Failed")
        print("\n💡 Next steps:")
        print("   1. Check hardware connections")
        print("   2. Verify car is on")
        print("   3. Try running with sudo: sudo python3 test_obd.py")
        print("   4. Check adapter compatibility with your vehicle")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
