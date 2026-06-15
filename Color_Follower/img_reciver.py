from multiprocessing import Value
from shutil import ExecError
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
        self.is_connected = False
        self.connect_at = 0
        self._connect()

    def _get_ip(self):
        try:
            file = open('rasPI_ip.txt' , 'r')
            ip = file.read()
            file.close()
        except Exception as e:
            print(f"Failed to open file | Error: {e}")
        if not ip.strip() : # no ip found
            print("No ip found")
            self.ip = input("Please enter your RasPi ip: ").lower()
            return
        else:
            a = input(f"is {ip} youre RasPi ip ?(y/n) ").lower()
            while a != 'y' and a != 'n': # unvalied entry (loop unnty true entry received)
                print("Please just sey (y/n) !!")
                a = input(f"is {ip} youre RasPi ip ?(y/n) ").lower()
            if a == 'y':
                self.ip = ip
                return self.ip
            elif a == 'n':
                self.ip = input ('Please enter your RasPi ip: ')
                return self.ip



    def _connect(self):
        try: # try to connect
            """Connect once (will be called only in __init__)"""
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            self.sock.settimeout(0.5)
            self.is_connected = True
            print(f"Connected to {self.ip}:{self.port}")
            return
        except Exception as e: # if failed try five times to connect
            print(f"Failed to connect !! | Error:{e}")
            print("retrying !!")
            self.connect_at += 1
            for _ in range(5):
                if self.connect_at >= 5:
                    print(f"Connecting attempt {self.connect_at}")
                    self._connect()
                else: return
        finally:
            file = open('rasPi_ip.txt' , 'w')
            file.write(self.ip)
            file.close()


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
            print("Connection closed")
