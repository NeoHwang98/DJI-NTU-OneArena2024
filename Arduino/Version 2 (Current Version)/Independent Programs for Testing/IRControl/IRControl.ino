//use original program, value > 1000000000
//Library for IR
#include "IRremote.h"

//setup IR
int receiver = 2;      // Signal Pin of IR receiver to Arduino Digital Pin 11
//The received value will be results.value

//Objects for IR
IRrecv irrecv(receiver);     // create instance of 'irrecv'
decode_results results;      // create instance of 'decode_results'



void setup(){
  Serial.begin(9600);
  irrecv.enableIRIn();           // Start the receiver
}



int n = 1;
void loop(){
  if (irrecv.decode(&results))   // have we received an IR signal? 
  { 
    Serial.print("Trial");
    Serial.print(n);
    Serial.println(results.value); //do whatever you want
    n = n + 1;
    delay(500);  // Do not get immediate repeat                 
    irrecv.resume();            // receive the next value
  }  
}


