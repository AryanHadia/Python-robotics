import cv2
from cv2.gapi.streaming import timestamp
import numpy as np
import time

# data saving
log_file = open('robot_coomands.txt' , 'w') # logfile opening
log_file.write("Time,command,x_position\n")

vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # capturing video from camera
if not vid.isOpened():
    raise ValueError("please check your camera")

# red color (hsv(hue, saturation, value))
lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 50, 50])
upper_red2 = np.array([180, 255, 255])

while True:
    ret, frame = vid.read()  # getting frame
    if not ret:
        print("Warning: Could not read frame")
        break  
    
    frame = cv2.flip(frame, 1)  # flipping frame
    height, width = frame.shape[:2]  # getting height and width of frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # turning rgb to hsv
    
    # making masks
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # removing noises 
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # finding (white) objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # moving robot
    command = None
    center_x = None

    for con in contours:
        area = cv2.contourArea(con)
        if area > 500:
            x, y, w, h = cv2.boundingRect(con)
            center_x = x + w // 2
            frame_center = width // 2
            
            if center_x > frame_center + 50:
                command = "Right"
            elif center_x < frame_center - 50:
                command = "Left"
            else:
                command = "Forward"
            
            # showing data
            if command:
                timestamp = time.strftime("%H:%M:%S")
                log_file.write(f"{timestamp},{command},{center_x}")
                log_file.flush() # saving data
            print(f"command: {command} at x={center_x}")
    
    cv2.imshow("red follower", frame)
    cv2.imshow("red mask", mask)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

log_file.close()
print("all comands saved")

vid.release()
cv2.destroyAllWindows()
