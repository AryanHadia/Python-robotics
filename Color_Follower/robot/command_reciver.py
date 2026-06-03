import socket
import serial
import time

ard_port = '/dev/ttyACM0'
boundrate = 9600

host = "0.0.0.0"
port = 5001


s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((host , port))
s.listen() # turn on listener
print("I'm listening")

# accept all
c,addr = s.accept()
print(f"connected by ({addr})")

# connection to arduino
try :
    arduino = serial.Serial(ard_port , boundrate , timeout=0.5) # connection to arduino
    time.sleep(4)  # timeout until arduino setup complete
    print (f"arduino connected on port {ard_port}")
except : # if arduino not found
    print(f"failed to fine Arduino on port {ard_port}")
    print("reciever simulation running ...")
    arduino = None

# recieve function
def receive():
    data = c.recv(1024) # receive 1024 byte of data
    if not data: 
        return None
    command = data.decode().strip()

    if arduino is not None:
        arduino.write(command.encode()) # sending command to Arduino
    else:
        print(f"[simualtion]: command= {command}")
    return command

while True:
    com = receive()
    if com == 'C': # close command
        break
print("connection close")
if arduino:
    arduino.close()