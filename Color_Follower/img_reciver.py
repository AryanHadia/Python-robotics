import socket
import numpy as np
import cv2
import time

class Receive:
    def __init__(self):
        self.ip = self._get_ip()
        self.port = 5000
        self.data = b''
        self.sock = None
        self._connect()

    def _get_ip(self):
        """Get IP once from file or user"""
        try:
            with open('raspi_ip.txt', 'r') as f:
                ip = f.read().strip()
                if ip:
                    return ip
        except:
            pass
        
        ip = input("Enter Raspberry Pi IP: ").strip()
        with open('raspi_ip.txt', 'w') as f:
            f.write(ip)
        return ip

    def _connect(self):
        """Connect once (will be called only in __init__)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.sock.settimeout(0.5)
        print(f"✅ Connected to {self.ip}:{self.port}")

    def receive_frame(self):
        """
        Get one frame.
        Returns None if connection lost.
        """
        while True:
            # 1. Search for JPEG markers in buffer
            start = self.data.find(b'\xff\xd8')
            end = self.data.find(b'\xff\xd9', start)
            
            if start != -1 and end != -1:
                # Complete frame found
                jpeg_data = self.data[start:end+2]
                self.data = self.data[end+2:]
                
                # Decode to OpenCV image
                np_arr = np.frombuffer(jpeg_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                return frame
            
            # 2. Need more data
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    print("Connection lost")
                    return None
                self.data += chunk
            except socket.timeout:
                # No data yet, continue loop
                continue
            except Exception as e:
                print(f"Socket error: {e}")
                return None

    def close(self):
        if self.sock:
            self.sock.close()
            print("🔌 Connection closed")