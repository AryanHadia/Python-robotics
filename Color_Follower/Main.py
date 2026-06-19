import cv2
from Colors import Colors_HSV as CH
from commands import CommandSender
import time
from img_reciver import Receive
import numpy as np
import random

class VisualCamera:
    def __init__(self):
        self.command_sender = CommandSender()
        self.receiver = Receive()
        self.width = None
        self.stuck_counter = 0
        self.last_move = None # last move by the robot


    def configuring_frame(self  , color):
        print("Ready to receive. Press 'q' to quit.")
        get_shape = self.get_shape()
        
        try:
            while True:
                # receiving frame
                frame = self.receiver.receive_frame()

                if frame is None: # if no frame found
                    print("Waiting for frame...")
                    time.sleep(0.01)
                    continue
                # getting brightness
                self.brightness(frame=frame)
                frame = np.clip(frame * self.brightness_factor, 0, 255).astype(np.uint8)

                
                height, self.width = frame.shape[:2]
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = CH().get_mask(hsv_=hsv, color_name=color)

                # removing noise
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                # finding contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                print("Contours found:", len(contours))

                # getting shape
                shape_ = self.shape_s(contours)
                print(f"shape = {shape_}")

                cv2.imshow("Robot Vision - Original", frame) # showing the main frame
                cv2.imshow("Robot Vision - Color Mask", mask) # showing the contours

                # check the shape
                if shape_ != get_shape: 
                    self.command_sender._send(b'L') # scan left
                    continue

                # count area
                self.area_contour(contours , shape_)


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.command_sender._send(b'S')
                    time.sleep(0.1)

                    

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
            return "triangle"

        elif corners == 4: # square or rectangle
            x, y, w, h =    cv2.boundingRect(approx)
            if h == 0:
                return "unknown"
            aspect = w / float(h)
            if 0.95 <= aspect <= 1.05:
                return "square"
            else:
                return "rectangle"

        elif corners == 5: # pentagon
            return "pentagon"
        
        elif corners >= 6: # circle
            return "circle"

        else:
            return "Unknown"
            
    
    def brightness(self , frame): # make a desicion to turn the light on or off
        gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        if brightness <= 50: # if its dark
            self.command_sender._send(b'N')
            self.brightness_factor = 4  # increasing the frame brightnes
        elif 50 < brightness <= 100: # if its not dark
            self.command_sender._send(b'M')
            self.brightness_factor = 3  # decreasing the frame brightnes
        elif 100 < brightness <= 150: # if its not dark
            self.command_sender._send(b'M')
            self.brightness_factor = 1.5  # increasing the frame brightnes
        else: # if its not dark
            self.command_sender._send(b'M')
            self.brightness_factor = 1  # decreasing the frame brightnes


    def area_contour(self, contours , f_shape): 
        self.stuck_permission = True
        if f_shape is None: # if no shape found
            if not contours:
                self.command_sender._send(b'L') # scan left
                return
            try:
                self.command_sender._send(b'L') # scan left

            except Exception as e: # if failed
                print(f"Failed to found area | Error: {e}")



        elif f_shape is not None: # if shape found
            if not contours:
                self.command_sender._send(b'L') # scan left
                return
            try:
                # calculating area
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)

                if area < 500: # small objects
                        self.movement(None , None , area)
                        self.command_sender._send(b'L') # scan left
                        return

                # founding center x and s
                x, y, w, h = cv2.boundingRect(largest)
                center_x = x + w // 2
                center_s = self.width // 2

                # founding distance
                if area < 29000:
                    dist = "Far"
                elif area > 35000:
                    dist = "Close"
                else:
                    self.stuck_permission = False
                    dist = "Norm"
                
                # getting data to processor
                self.command_sender.processor(center_x=center_x , center_s=center_s , dist=dist , shape=f_shape)

                if self.stuck_permission is True:
                    # saving the movement
                    self.movement(dist , center_x , area)
                else:
                    self.save_movement(dist , center_x , area)

            except Exception as e: # if failed
                print(f"Failed to found area | Error: {e}")


    def options(self): # return available options
        op = ['color follow' , 'shape follow']
        return op

    def movement(self , dist , center_x , Area): # record the movement
        move = (dist , center_x // 20 , int(Area // 1000))
        if self.last_move is None: # if it's the first move
            self.last_move = move
            return
        else:
            if self.last_move != move:
                self.last_move = move
                self.stuck_counter = 0 # resetting stuck counter
                return
            else:
                if self.stuck_counter >= 15: # if stuck for 15 times
                    self.stuck_counter = 0 # resetting stuck counter
                    self.command_sender._send(b'B') # scan back
                    time.sleep(1)
                    choice = random.choice([b'L' , b'R']),
                    time.sleep(1)
                    self.command_sender._send(choice)
                else:
                    self.stuck_counter += 1 # adding stuck counter
                return
    
    def save_movement(self , dist , center_x , Area): # save the movement to the file
        self.last_move = (dist , center_x // 20 , int(Area // 1000))
                
