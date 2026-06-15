import socket


class command_sender:
    def __init__(self):
        self.port = 5001
        self.s = None
        self.is_connected = False
        self._connect()

    
    def com_save(self , com): # saving sended commands 
        file = open('Command.txt' , 'a') # opening file
        if not file: 
            print("Failed to save command (no Command.txt found) :( ")
            return None

        
        
        file.write(f"{com}\n") # write command
        file.close()
        

    def _get_ip(self): # getting ip from last connection
        ip_file = 'rasPI_ip.txt'
        file = open(ip_file , 'r') # reading from svaed ip
        ip = file.read()
        return ip


    def _connect(self): # connecting
        try: # try connectiong
            ip = self._get_ip()
            s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.s = s
            self.s.connect((ip , self.port))
            self.is_connected = True
            print(f"connected on {ip}:{self.port}") 
        except Exception as e: # if not connected
            print(f'Failed to connect !! | Error: {e}')
            print("Running on simulation mode ...")
            self.is_connected = False

    
    def send(self , command): # sending commands
        if self.is_connected is True: # if connected
            try:
                self.com_save(command) # save the command
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
