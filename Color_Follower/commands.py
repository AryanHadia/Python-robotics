from command_sender import command_sender
import time

class CommandSender:
    def __init__(self):
        self.robot = command_sender()
        # فقط ۲ ثانیه برای اطمینان از آماده شدن آردوینو (اختیاری، چون connection خودش منتظر READY می‌ماند)
        time.sleep(2)

    def processor(self, center_x, center_s, dist):
        if center_x is None:
            self._send(b'L')   # scan left(for finding color)
            return

        if center_x > center_s + 100:
            self._send(b'R')   # turn right
        elif center_x < center_s - 100:
            self._send(b'L')   # turn left
        elif center_s + 50 < center_x < center_s + 100:
            self._send(b'R')   # scan right
        elif center_s - 100 < center_x < center_s - 50:
            self._send(b'L')   # scan left
        elif dist == "Far":
            self._send(b'F')   # forward
        elif dist == "Close":
            self._send(b'B')   # Bakward
        else:
            self._send(b'S')   # stop

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
