import cv2
from Colors import Colors_HSV as CH
from commands import CommandSender

class VisualCamera:
    def __init__(self):
        self.command_sender = CommandSender()
        self.width = None
        self.camera_index = None

    def camera_connect(self):
        for i in range(0, 5):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"Camera found on index {i}")
                    self.camera_index = i
                    cap.release()
                    return cv2.VideoCapture(i, cv2.CAP_DSHOW)
            cap.release()
        raise ValueError("No camera found!")

    def configuring_frame(self, color):
        if color not in CH().colors_list():
            raise ValueError(f"Color '{color}' is not valid")

        cap = self.camera_connect()
        if not cap.isOpened():
            raise ValueError("Failed to open camera")

        print("Camera ready. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to get frame, retrying...")
                continue

            if frame is None:
                continue

            height, self.width = frame.shape[:2]
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = CH().get_mask(hsv_=hsv, color_name=color)

            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.area_contour(contours)

            # Show both windows
            cv2.imshow("Robot Vision - Original", frame)
            cv2.imshow("Robot Vision - Color Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
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