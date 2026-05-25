# confiquring color data for 

import numpy as np
import cv2


class Colors_HSV(): # colors HSV data for opencv projects
    # فقط یک دیکشنری ساده  
    def __init__(self) -> None: 
        self.COLORS_HSV = {
        'red': [(np.array([0,50,50]), np.array([10,255,255])),
                (np.array([160,50,50]), np.array([180,255,255]))],
        'blue': [(np.array([100,50,50]), np.array([130,255,255]))],
        'green': [(np.array([40,50,50]), np.array([80,255,255]))],
        'purple': [(np.array([130,50,50]), np.array([160,255,255]))],
        'yellow': [(np.array([20,50,50]), np.array([35,255,255]))],
        'orange': [(np.array([5,50,50]), np.array([15,255,255]))],
        'brown': [(np.array([10,50,20]), np.array([20,255,100]))]
        }

    def get_mask(self , hsv_, color_name):
        masks = []
        for lower, upper in self.COLORS_HSV[color_name]:
            masks.append(cv2.inRange(hsv_, lower, upper))
        return cv2.bitwise_or(masks[0], masks[1]) if len(masks) > 1 else masks[0]
    
    def colors_list(self): # colors list
        return ("red" , "blue" , "green" , "purple" , "yellow" , "orange" , "brown")