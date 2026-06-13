import cv2
from Colors import Colors_HSV as CH
from commands import CommandSender
import time
from img_reciver import Receive
import numpy as np

class VisualCamera:
    def __init__(self):
        self.command_sender = CommandSender()
        self.receiver = Receive()
        self.width = None


    def configuring_frame(self  , color):
        print("Ready to receive. Press 'q' to quit.")
        get_shape = self.get_shape()
        
        try:
            while True:
                frame = self.receiver.receive_frame()
                
                if frame is None:
                    print("Waiting for frame...")
                    time.sleep(0.01)
                    continue
                brightness_factor = 1.2  # increasing the frame brightnes
                frame = np.clip(frame * brightness_factor, 0, 255).astype(np.uint8)

                height, self.width = frame.shape[:2]
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = CH().get_mask(hsv_=hsv, color_name=color)

                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                shape_ = self.shape_s(contours)
                if get_shape != shape_: # if it's not the user shape
                    continue
                self.area_contour(contours , shape_)

                cv2.imshow("Robot Vision - Original", frame) # showing the main frame
                cv2.imshow("Robot Vision - Color Mask", mask) # showing the contours

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.command_sender.send(b"S")
                    time.sleep(0.1)
                    break

        finally: # in the final
            self.command_sender.close()
            self.receiver.close()   
            cv2.destroyAllWindows()
            print("Camera released")


    def get_shape(self): # getting shape from user
        print("select a shape to follow")
        shapes = ('circle' , 'triangle' , 'square' , 'rectangle' , 'pentagon')
        shape = input("Please select one (circle , triangle , square , rectangle , pentagon): ").lower()
        while shape not in shapes : # unknown shapes
            print("Please enter a valied shape")
            shape = input("Please select one (circle , triangle , square , rectangle , pentagon): ").lower()
        return shape

    
    def shape_s(self, contours): # finding shapes
        if not contours:
            return None
            
        # finding largest contour
        contour = max(contours, key=cv2.contourArea)

        peri = cv2.arcLength(contour , True)
        approx = cv2.approxPolyDP(contour , 0.04 * peri, True)
        corners = len(approx)

        # Returning the shape name
        if corners == 3: # if there was 3 corners
            return "Triangle"

        elif corners == 4: # square or rectangle
            x, y, w, h =    cv2.boundingRect(approx)
            if h == 0:
                return "Unknown"
            aspect = w / float(h)
            if 0.95 <= aspect <= 1.05:
                return "Square"
            else:
                return "Rectangle"

        elif corners == 5: # pentagon
            return "Pentagon"
        
        elif corners >= 6: # circle
            return "Circle"

        else:
            return "Unknown"


    def area_contour(self, contours , f_shape):        
        if self.width is None:
            return

        if not contours:
            self.command_sender.processor(None, self.width//2, None)
            return

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < 500:
            self.command_sender.processor(None, self.width//2, None)
            return

        x, y, w, h = cv2.boundingRect(largest)
        center_x = x + w // 2
        center_s = self.width // 2

        if area < 29000:
            dist = "Far"
        elif area > 35000:
            dist = "Close"
        else:
            dist = "Norm"

        self.command_sender.processor(center_x, center_s, dist , f_shape)

    def options(self): # return available options
        op = ['color follow' , 'shape follow']
        return op
