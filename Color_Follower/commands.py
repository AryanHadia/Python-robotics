from Arduino_connect import Arduino

class CommandSender:
    def __init__(self):
        self.robot = Arduino()
        self.robot.connection()
        self.last_command = None

    def processor(self, center_x, center_s, dist):
        if center_x is None:
            self._send(b"Scan_left\n")
            return


        if center_x > center_s + 100:
            self._send(b"Turn_right\n")
        elif center_x < center_s - 100:
            self._send(b"Turn_left\n")
        elif center_s + 50 < center_x < center_s + 100:
            self._send(b"Scan_right\n")
        elif center_s - 100 < center_x < center_s - 50:
            self._send(b"Scan_left\n")
        else:
            if dist == "Far":
                self._send(b"Forward\n")
            elif dist == "Close":
                self._send(b"Backward\n")
            else:
                self._send(b"Stop\n")

    def _send(self, command):
        if command != self.last_command:
            time.sleep(0.05)  # کمی تأخیر بین فرمان‌ها
            self.robot.send_command(command)
            self.last_command = command

    def close(self):
        self.robot.disconnect()