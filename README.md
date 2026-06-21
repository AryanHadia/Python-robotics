# Color Follower robot
- A robot that can follow a specific color and shape in a video feed (version 1.0)

## Robot parts
- Arduino(uno)
- L298n (motor Driver)
- Two geared motor
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
8) If the robot lost the target, it will return to the initial position

## How to use
1) Run the program (when your robot is ready)
2) Select a color
3) Select a shape
3) Place your object in front of webcam


## Challenges
- Low light environments
- Object loss recovery
- Robot jam detection
- Wireless latency
### Robot jam detection
- Detect when the robot is stuck in a position
- Implement a escape algorithm to move out of the jam position
- Detecting by the center_x and distance to the target
### Wireless latency
- If the raspberry pi is not connected to the internet by dungle, it can cause latency in conncetion.
- It can be improved with dungle


## Dependencies
- [Python 3.7+](https://www.python.org/downloads/)
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [Pyserial](https://pyserial.readthedocs.io/en/latest/)

## Features
- Color detection using HSV masks
- Shape detection (Circle, Triangle, Square, Rectangle, Pentagon)
- Automatic brightness compensation
- Object tracking
- Lost-target recovery system
- Stuck detection and escape algorithm
- Wireless communication between robot and PC
- Lighting compensation
- Distance measurement


## Note 
- Good lighting helps with color detection accuracy
- Adjust COM port in Arduino_connect.py if needed
