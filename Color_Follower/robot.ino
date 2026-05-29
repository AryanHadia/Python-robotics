int m1p1 = 5;
int m1p2 = 3;
int m2p1 = 6;
int m2p2 = 9;

void setup() {
    Serial.begin(9600);
    pinMode(m1p1, OUTPUT);
    pinMode(m1p2, OUTPUT);
    pinMode(m2p1, OUTPUT);
    pinMode(m2p2, OUTPUT);
    stop();
}

void loop() {
    if (Serial.available() > 0) {
        String cmd = Serial.readString();
        cmd.trim();
        
        if (cmd == "Forward") {
            forward();
        }
        else if (cmd == "Backward") {
            backward();
        }
        else if (cmd == "Stop") {
            stop();
        }
        else if (cmd == "Turn_right") {
            turnRight();
        }
        else if (cmd == "Turn_left") {
            turnLeft();
        }
        else if (cmd == "Scan_left") {
            scanLeft();
        }
        else if (cmd == "Scan_right") {
            scanRight();
        }
    }
}

void forward() {
    analogWrite(m1p1, 60);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 60);
    analogWrite(m2p2, 0);
}

void backward() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 60);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 60);
}

void stop() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 0);
}

void turnRight() {
    // چرخش به راست بدون توقف خودکار
    analogWrite(m1p1, 60);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 60);
    // حذف delay و stop
}

void turnLeft() {
    // چرخش به چپ بدون توقف خودکار
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 60);
    analogWrite(m2p1, 60);
    analogWrite(m2p2, 0);
    // حذف delay و stop
}

void scanLeft() {
    // اسکن به چپ (آهسته) بدون توقف خودکار
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 40);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 0);
}

void scanRight() {
    // اسکن به راست (آهسته) بدون توقف خودکار
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 40);
}