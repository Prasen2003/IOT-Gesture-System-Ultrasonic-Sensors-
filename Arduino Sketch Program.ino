#define TRIG_PIN1 9  // Set the trig pin for sensor 1
#define ECHO_PIN1 10 // Set the echo pin for sensor 1
#define TRIG_PIN2 11 // Set the trig pin for sensor 2
#define ECHO_PIN2 12 // Set the echo pin for sensor 2

long readUltrasonicDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2); 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH, 30000);  // Timeout after 30 ms to prevent hanging
  if (duration == 0) {
    return -1;  // Return -1 if no signal is received (timeout)
  }
  
  return duration / 58.0;  // Convert the time to distance (in cm)
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
}

void loop() {
  long distance1 = readUltrasonicDistance(TRIG_PIN1, ECHO_PIN1);  // Trigger sensor 1
  delay(50);  // Small delay before triggering the next sensor to avoid interference
  long distance2 = readUltrasonicDistance(TRIG_PIN2, ECHO_PIN2);  // Trigger sensor 2
  
  if (distance1 == -1) {
    distance1 = 0;  // Set to 0 if sensor 1 times out
  }
  if (distance2 == -1) {
    distance2 = 0;  // Set to 0 if sensor 2 times out
  }

  Serial.print(distance1);
  Serial.print(",");
  Serial.println(distance2);

  delay(100);  // Adjust the delay if needed
}
