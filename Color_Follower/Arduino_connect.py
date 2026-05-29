"""
Arduino controlling Module - Auto Port Finding
"""
import serial
import serial.tools.list_ports
import time

class Arduino:
    def __init__(self, baudrate=9600):
        self.baudrate = baudrate
        self.serial_connection = None
        self.is_connected = False
        self.last_command = None
        self.port = None
        
    def find_port(self):
        """Automatically find Arduino port"""
        print("Searching for Arduino...")
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            if "Arduino" in port.description or "USB Serial" in port.description:
                print(f"Found Arduino on {port.device} ({port.description})")
                return port.device
        
        common_ports = ['COM3', 'COM4', 'COM5', 'COM6', '/dev/ttyUSB0', '/dev/ttyACM0']
        for port_name in common_ports:
            try:
                test_serial = serial.Serial(port_name, self.baudrate, timeout=0.5)
                test_serial.close()
                print(f"Found device on {port_name}")
                return port_name
            except:
                continue
        
        print("No Arduino found!")
        return None
        
    def connection(self):
        """Establish connection to Arduino (auto port detection)"""
        if self.port is None:
            self.port = self.find_port()
            if self.port is None:
                print("Could not find Arduino. Running in SIMULATION mode.")
                self.is_connected = False
                return False
        
        try:
            if self.serial_connection and self.serial_connection.is_open:
                return True  # Already connected
            
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            self.is_connected = True
            print(f"Connected to Arduino on {self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to Arduino on {self.port}")
            print(f"   Error: {e}")
            self.is_connected = False
            return False

    def send_command(self, command):
        """Send command to Arduino - command must be bytes like b'Forward\\n'"""
        if not command:
            return False

        # Make sure we're connected
        if not self.is_connected or not self.serial_connection:
            if not self.connection():
                print(f"🔸 [SIMULATION] Command: {command}")
                return False

        # Don't send duplicate commands (except Stop)
        if command == self.last_command and command != b"Stop\n":
            return True

        try:
            self.serial_connection.write(command)
            self.last_command = command
            print(f"📡 Sent RAW: {command}")  # چاپ خام فرمان برای دیباگ
            return True
        except Exception as e:
            print(f"❌ Failed to send command | Error: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Close connection"""
        if self.is_connected and self.serial_connection:
            self.send_command(b"Stop\n")
            self.serial_connection.close()
            print("Disconnected from Arduino")

    # ========== Commands ==========
    def turn_right(self):
        return self.send_command(b"Turn_right\n")

    def turn_left(self):
        return self.send_command(b"Turn_left\n")

    def scan_right(self):
        return self.send_command(b"Scan_right\n")

    def scan_left(self):
        return self.send_command(b"Scan_left\n")

    def stop(self):
        return self.send_command(b"Stop\n")

    def forward(self):
        return self.send_command(b"Forward\n")

    def backward(self):
        return self.send_command(b"Backward\n")
