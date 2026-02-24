


//Control for motors
int speed = 100; //From 0 to 255


//Setup for motors
// Motor 1 connections
int enA = 9; //speed
int in1 = 8; //terminal 1
int in2 = 7; //terminal 2

// Motor 2 connections
int enB = 3; //speed
int in3 = 5; //terminal 1
int in4 = 4; //terminal 2



void setup() {
  //MOTOR
  //Set pin for motor
  pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
  //Turn off motors
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);
  //Set motor speed
  analogWrite(enA, speed);
	analogWrite(enB, speed);
}

void loop() {
  delay(3000);
  forward();
  delay(3000);
  stop();
  delay(750);
  backward();
  delay(3000);
  stop();
}

//for motor
void forward() {
  digitalWrite(in1, HIGH);
	digitalWrite(in2, LOW);
	digitalWrite(in3, HIGH);
	digitalWrite(in4, LOW);
}

void backward() {
  digitalWrite(in1, LOW);
	digitalWrite(in2, HIGH);
	digitalWrite(in3, LOW);
	digitalWrite(in4, HIGH);
}

void stop() {
  digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);
}

