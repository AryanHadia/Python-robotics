import socket
import os

class command_sender:
    def __init__(self):
        self.port = 5001
        self.s = None
        self.is_connected = False
        self._connect()
        

    def _get_ip(self): # getting ip from last connection
        ip_file = 'rasPI_ip.txt'

        # if file exist
        if os.path.exists(ip_file):
            with open(ip_file, 'r') as f:
                ip = f.read().strip()
                if ip:
                    return ip
        # if no ip found
        input("please enter your raspi ip: ").strip()
        return ip


    def _connect(self): # connecting
        try: # try connectiong
            ip = self._get_ip()
            s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.s = s
            self.s.connect((ip , self.port))
            print(f"connected on {ip}:{self.port}") 
        except Exception as e: # if not connected
            print(f'Failed to connect !! | Error: {e}')
            print("Running on simulation mode ...")
            self.is_connected = False

    
    def send(self , command): # sending commands
        if self.is_connected is True: # if connected
            try:
                self.s.sendall(command) # send command to all
                print(f"sent: {command}")
            except Exception as e: # if failed to send command
                print(f"Failed to send command | Error: {e}")
        
        else:
            print(f"[simulation]: {command}")


    def close(self): # closing connection
        if self.s:
            self.s.close()
            print("connection closed !!")
        self.is_connected = False