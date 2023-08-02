int x;
int led = 2;
int g = 3;
int incomingByte;
void setup() {
 pinMode(led,OUTPUT);
 pinMode(g,OUTPUT);
 pinMode(13,OUTPUT);
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
 if (Serial.available()) {
    incomingByte = Serial.read();
    if (incomingByte == 'H') {
      digitalWrite(led, HIGH);
      digitalWrite(g, LOW);
      delay(5000);
    }
    if (incomingByte == 'L') {
      digitalWrite(led, LOW);
      digitalWrite(g, LOW);
    }
  }
}