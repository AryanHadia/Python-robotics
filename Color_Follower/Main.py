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

    def configuring_frame(self, color):
        if color not in CH().colors_list():
            raise ValueError(f"Color '{color}' is not valid")

        print("Camera ready. Press 'q' to quit.")
        
        try:
            while True:
                frame = self.receiver.receive_frame()
                
                if frame is None:
                    print("Waiting for frame...")
                    time.sleep(0.01)
                    continue
                brightness_factor = 1.5   # هرچی این عدد بیشتر باشه، تصویر روشن‌تر می‌شه (حدود 1.3 تا 1.8 مناسب)
                frame = np.clip(frame * brightness_factor, 0, 255).astype(np.uint8)

                height, self.width = frame.shape[:2]
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = CH().get_mask(hsv_=hsv, color_name=color)

                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                self.area_contour(contours)

                cv2.imshow("Robot Vision - Original", frame)
                cv2.imshow("Robot Vision - Color Mask", mask)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.command_sender.robot.send_command(b"S")
                    time.sleep(0.1)
                    break

        finally:
            self.command_sender.close()
            self.receiver.close()   
            cv2.destroyAllWindows()
            print("Camera released")

    def area_contour(self, contours):
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

        if area < 1500:
            dist = "Far"
        elif area > 5000:
            dist = "Close"
        else:
            dist = "Norm"

        self.command_sender.processor(center_x, center_s, dist)