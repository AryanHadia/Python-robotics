import cv2
from Colors import Colors_HSV as CH
from Arduino_connect import Arduino as Ac
import time

# functions
def time_show():
    return time.strftime("%H:%M:%S")

# logfile 
logfile = open("Colors Followed" , "w") # opening text file to save commands
logfile.write("time/color/center_x/Time\n") 

# camera opening
def find_camra():
    for x in range(0,5):
        vid = cv2.VideoCapture(x , cv2.CAP_DSHOW) # trying to recive frame of camera
        if vid.isOpened(): # if camera opens
            return vid # returning camera

vid = find_camra()
color = input("choose your color(red , green , blue , yellow , purple , orange , brown): ")
while color not in CH().colors_list(): 
    print("please select one of the options !!")
    color = input("choose your color(red , green , blue , yellow , purple , orange , brown): ")

robot = Ac()
robot.connection()

while True:
    ret, frame = vid.read() # taking a frame of camra
    if not ret:
        raise ValueError ("Failed to get a frame")
    
    frame = cv2.flip(frame, 1)  # flipping frame
    height, width= frame.shape[:2] 
    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV) # turning BGR to HSV
    
    mask = CH().get_mask(hsv_=hsv , color_name=color) # getting mask
    
    # countors
    countors, _ = cv2.findContours(mask , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    # removing noise 
    mask = cv2.erode(mask , None , iterations=2)
    mask = cv2.dilate(mask , None , iterations=2)

    # center_x and command variables
    command = None
    center_x = None

    for con in countors:
        Area = cv2.contourArea(con) # finding area of contour

        if Area > 800:
            x, y, w, h = cv2.boundingRect(con)
            center_x = x + w // 2
            frame_center = width // 2
            if frame_center + 100 > center_x > frame_center + 50:
                command = "Scan_right"
                robot.scan_right()
                logfile.write(f"{command} , {time_show()} \n")
                logfile.flush() # saving changes

            elif frame_center - 100 < center_x < frame_center - 50:
                command = "Scan_left"
                robot.scan_left()
                logfile.write(f"{command} , {time_show()} \n")
                logfile.flush() # saving changes

            elif center_x > frame_center + 100:
                command = "Turn_right"
                robot.turn_right
                logfile.write(f"{command} , {time_show()} \n")
                logfile.flush() # saving changes

            elif center_x < frame_center - 100:
                command = "Turn_left"
                robot.turn_left
                logfile.write(f"{command} , {time_show()} \n")
                logfile.flush() # saving changes

            else:
                command = "stop"
                robot.stop()
                logfile.write(f"{command} , {time_show()} \n")
                logfile.flush() # saving changes

    cv2.imshow("camera" , frame)
    cv2.imshow("colors" , mask)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

logfile.close()
print("all comands saved")

vid.release()
cv2.destroyAllWindows()