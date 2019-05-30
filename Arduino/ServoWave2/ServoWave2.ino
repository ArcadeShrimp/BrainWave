/* This program reads an integer input from 0 to 100 from the serial monitor and makes a 
 *  Servo motor wave at a speed proportional to the input. */

#include <Servo.h>

#define REQUIRED_TIMEOUT 100
#define SERVO_PIN 8
#define DELAY 10
#define RIGHT_POSITION_LIMIT 70
#define LEFT_POSITION_LIMIT 160

Servo servo;
int Position=RIGHT_POSITION_LIMIT, input=1;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(REQUIRED_TIMEOUT);
  servo.attach(SERVO_PIN);
  servo.write(RIGHT_POSITION_LIMIT);
  delay (DELAY);
}

void loop() {

//Check that the input is non zero, if yes, then start waving. 
//Check for any new input for every position increment.

if(input!=0){
  
  // Wave in counter clockwise direction.
  
  while(Position<LEFT_POSITION_LIMIT){
    Position=Position+input;                      // Increment the position by a step size aquired from the input.
    servo.write(Position);
    serialEvent();                                // Check for any new input for every position increment.
    if(input==0) break;                           // If input is zero, stop waving.
    delay(DELAY);  
  }
  // Wave in clockwise direction.
  while(Position>RIGHT_POSITION_LIMIT){               
    Position=Position-input;
    servo.write(Position);
    serialEvent();                                // Check for any new input for every position increment.
    if(input==0) break;                           // If input is zero, stop waving.
    delay(DELAY); 
    }
}

  }
/* serialEvent() is a function that will be called on every time we want to check 
 * if something was written to the buffer and store the value as an integer 
 * "input" which will be used to determine the speed of the waving of the Servo.*/
void serialEvent () {
    if(Serial.available()>0)
    {
      input=Serial.parseInt();
      input=input/10;                   // Truncate the input to a value from 0 to 10,
    }                                   // which will be used to increment the Servo position.
  
  }
