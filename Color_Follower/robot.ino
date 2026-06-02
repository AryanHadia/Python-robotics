int m1p1 = 3;
int m1p2 = 5;
int m2p1 = 6;
int m2p2 = 9;
int CL = 4;
int motor_speed;
int scan_speed;

void setup() {
    motor_speed = 90;
    scan_speed = 40;
    Serial.begin(9600);
    pinMode(m1p1, OUTPUT);
    pinMode(m1p2, OUTPUT);
    pinMode(m2p1, OUTPUT);
    pinMode(m2p2, OUTPUT);
    pinMode(CL, OUTPUT);
    stop();
    Serial.println("READY");   
}

void loop() {
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        while (Serial.available()) Serial.read();
  
        switch (cmd) {
            case 'F': forward(); break;
            case 'B': backward(); break;
            case 'R': turnRight(); break;
            case 'L': turnLeft(); break;
            case 'S': stop(); break;
            case 'E': scanRight(); break;   
            case 'W': scanLeft(); break;    
            case 'N': lightOn(); break;     
            case 'M': lightOff(); break;    
        }
    }
}

void forward() {
    analogWrite(m1p1, motor_speed);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, motor_speed);
    analogWrite(m2p2, 0);
}

void backward() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, motor_speed);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, motor_speed);
}

void stop() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 0);
}

void turnRight() {
    analogWrite(m1p1, motor_speed);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, scan_speed);
}

void turnLeft() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, scan_speed);
    analogWrite(m2p1, motor_speed);
    analogWrite(m2p2, 0);
}

void scanLeft() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, scan_speed);
    analogWrite(m2p2, 0);
}

void scanRight() {
    analogWrite(m1p1, scan_speed);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 0);
}

void lightOn() {
    digitalWrite(CL, HIGH);
}

void lightOff() {
    digitalWrite(CL, LOW);
}
