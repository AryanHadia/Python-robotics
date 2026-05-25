# Color Follower robot

## Robot parts
- Arduino(uno)
- L298n (motor Driver)
- One geared motor
- Window or linux or mac (For Python files)
- Webcam

## How it workes
1) Taking a frame of camera
2) Getting one option(color) from user ( red , green , blue , yellow , orange , ...)
3) Finding that color in frame
4) Turn the object color to white
5) Connect to Arduino
6) Sent command to Arduino
7) Robot moves ...

## How to use
1) Run the program (when your robot is ready)
2) Select a color
3) Place your object in front of webcam

## Dependencies
- python 3.7+
- OpenCV
- NumPy
- Pyserial

## Note 
- Good lighting helps with color detection accuracy
- Adjust COM port in Arduino_connect.py if needed