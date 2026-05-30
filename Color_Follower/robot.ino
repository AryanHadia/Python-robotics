int led1 = 2;
int led2 = 3;

void setup() {
    Serial.begin(9600);
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    stop();
    Serial.println("READY");   
}

void loop() {
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        while (Serial.available()) Serial.read();

  
        switch (cmd) {
            case 'F':   // Forward
                forward();
                break;
            case 'B':   // Backward
                backward();
                break;
            case 'R':   // Turn Right
                turnRight();
                break;
            case 'L':   // Turn Left
                turnLeft();
                break;
            case 'S':   // Stop
                stop();
                break;
            case 'SR': // scan right
                stop();
                break;
            case 'SL': // scan left
                stop();
                break;
        }
    }
}

void forward() {
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
}

void backward() {
    digitalWrite(led1, HIGH);   
    digitalWrite(led2, HIGH);
}

void stop() {
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
}

void turnRight() {
    digitalWrite(led1, HIGH);
    digitalWrite(led2, LOW);
}

void turnLeft() {
    digitalWrite(led1, LOW);
    digitalWrite(led2, HIGH);
}

void scanleft() {
    digitalWrite(led1, LOW);
    digitalWrite(led2, HIGH);
}

void scanright() {
    digitalWrite(led1, HIGH);
    digitalWrite(led2, LOW);
}
