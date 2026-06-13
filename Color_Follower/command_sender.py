from command_sender import command_sender
import time

class CommandSender:
    def __init__(self):
        self.robot = command_sender()

    def processor(self, center_x, center_s, dist , shape):
        if shape is None: # if no shape found
            self._send(b"E") # scan left
            time.sleep(0.5) # wait 1 second
            self._send(b"W")
            return
    
        if center_x > center_s + 100: # turn right
            self._send(b"R")
        elif center_x < center_s - 100: # turn left
            self._send(b"L")
        elif center_s + 50 < center_x < center_s + 100: # scan right
            self._send(b"E")
        elif center_s + 10 < center_x < center_s + 50: # slowly scan right
            self._send(b"E")
        elif center_s - 10 > center_x > center_s - 50: # slowly scan left
            self._send(b"W")
        elif center_s - 50 > center_x > center_s - 100: # scan left
            self._send(b"W")
        else: # stop
            if dist == "Far": # forward
                self._send(b"F")
            elif dist == "Close": # Backward
                self._send(b"B")
            else: # stop
                self._send(b"S")
        return 

    def _send(self, command_bytes):
        self.robot.send(command_bytes)


    def close(self):
        """Stop robot and close connection"""
        try:
            self.robot.send(b"S")  
            time.sleep(0.05)
        except Exception as e:
            print(f"Stop error: {e}")
        finally:
            self.robot.close()
