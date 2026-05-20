def send_command_with_retry(command, retries=3):
    """Send command to Arduino with retry mechanism"""
    for i in range(retries):
        arduino.write(command.encode())
        time.sleep(0.1)
        if arduino.in_waiting:
            response = arduino.readline().decode().strip()
            return response
        print(f"Retry {i+1}/{retries}...")
    return "No response"
