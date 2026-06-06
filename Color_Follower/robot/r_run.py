import subprocess
import time
import signal
import sys
import os


CAMERA_DEVICE = '/dev/video0'
STREAM_PORT = 5000
COMMAND_PORT = 5001


PYTHON_VENV = '/home/aryan/myenv/bin/python3'


COMMAND_RECEIVER_PATH = '/home/aryan/c_receiver.py'  # ← این را به مسیر واقعی تغییر بده

processes = []

def cleanup():
    print("\nStopping all processes...")
    for p in processes:
        try:
            p.terminate()
        except:
            pass
    time.sleep(1)
    for p in processes:
        try:
            if p.poll() is None:
                p.kill()
        except:
            pass
    print("All processes stopped")
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    print("Starting Robot System on Raspberry Pi...")
    

    print(f"Starting camera stream on port {STREAM_PORT}...")
    stream_cmd = f"ffmpeg -f v4l2 -framerate 15 -video_size 640x480 -i {CAMERA_DEVICE} -f mjpeg - 2>/dev/null | nc -l -p {STREAM_PORT}"
    p1 = subprocess.Popen(stream_cmd, shell=True, preexec_fn=os.setsid)
    processes.append(p1)
    print("Camera stream started")
    time.sleep(2)
    
    print(f"Starting command server on port {COMMAND_PORT}...")
    p2 = subprocess.Popen([PYTHON_VENV, COMMAND_RECEIVER_PATH], preexec_fn=os.setsid)
    processes.append(p2)
    print("Command server started")
    
    print("\nRobot is ready!")
    print(f"   - Camera stream: port {STREAM_PORT}")
    print(f"   - Command server: port {COMMAND_PORT}")
    print("   - Press Ctrl+C to stop\n")
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
