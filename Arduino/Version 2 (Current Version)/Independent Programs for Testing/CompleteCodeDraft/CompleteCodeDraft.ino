//Library for IR
#include "IRremote.h"
//library for US
#include <NewPing.h>


//Setup IR
int receiver = 2; 
//The received value will be results.value

//Objects for IR
IRrecv irrecv(receiver);     // create instance of 'irrecv'
decode_results results;      // create instance of 'decode_results'


//Setup for US 
//US connections
#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.

//Control for US
#define MAX_DISTANCE 100 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

//The ping function
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.


//Control for motors
int speed = 255; //From 0 to 255

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
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.:

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

  irrecv.enableIRIn();
}

void loop() {
  if (irrecv.decode(&results))   // have we received an IR signal? 
  { 
    Serial.println("Triggered");
    //open
    if (sonar.ping_cm()>=7){
      backward();  
    }
    //stop opening
    while (true){
      if (sonar.ping_cm()<=5){
        stop();
        break;
      }
      delay(50);
    }
    //wait for closing
    delay(5000);
    //closing
    forward();
    //stop closing
    while (true){
      if (sonar.ping_cm()>=45){
        stop();
        break;
      }
    }                 
  }
  irrecv.resume();        // receive the next value
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


