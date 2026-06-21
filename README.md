# OpenCV-Robotics

Computer vision projects for my robots.  
This is where I learn to give **eyes** to my robots.

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

## Projects

### 1. Color Detection (`color_detection.py`)
- **What it does:** Detects blue color in an image and draws a rectangle around it.
- **Why it matters:** First step toward object tracking for my robot.
- **Next step:** Replace test image with real camera feed.

### 2. Color Follower (`run.py`)
- **What it does:** Follows specific color and shape in a video feed.
- **Why it matters:** Second step toward object tracking for my robot.
- **Next step:** Add more features like lighting compensation and distance measurement.

## How to Run

1. Install OpenCV:
   ```bash
   pip install opencv-python numpy
2. Install Pyserial:
   ```bash
   pip install pyserial
   ```
3. Connect Arduino to Raspberry Pi or PC

4. Run the program:
   ```bash
   python run.py
   ```
