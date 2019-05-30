/* This program reads an integer input from 0 to 100 from the serial monitor and
   makes a Servo motor wave at a speed proportional to the input. */

#include <Servo.h>

#define REQUIRED_TIMEOUT 100
#define SERVO_PIN 8
#define DELAY 1000
#define RIGHT_POSITION_LIMIT 70
#define LEFT_POSITION_LIMIT 160
Servo servo;
int Position=RIGHT_POSITION_LIMIT, Delay=100, input=1;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(REQUIRED_TIMEOUT);
  servo.attach(SERVO_PIN);
  servo.write(RIGHT_POSITION_LIMIT);
  delay (DELAY);
}

void loop() {

  //Check that the input is non zero, if yes, then start waving. 
  
  if(input!=0){
    
    // Wave counter clockwise.
    
    for(Position; Position<LEFT_POSITION_LIMIT;Position++){            
      servo.write(Position);
      serialEvent();                  //Check for any new input for every position increment.
      if(input==0) break;             //if input is zero, stop waving.
      delay(Delay);                   // delay each position increment by d, the mapped input.
  }
    
    // Wave clockwise.
    
    for(Position;Position>RIGHT_POSITION_LIMIT;Position--){                  
      servo.write(Position);
      serialEvent();                  // Check for any new input for every position increment.
      if(input==0) break;             // if input is zero, stop waving
      delay(Delay);                   // delay each position increment by d, the mapped input.
    }
}

  }
/* serialEvent() is a function that will be called on every time we want to check if something  
 *  was written to the buffer and store the value as an integer "input" which will be used to 
    determine the speed of the waving of the Servo.*/
void serialEvent () {
  if(Serial.available()>0){
      input=Serial.parseInt();

/*map the input from [0,100] to [99,0] in order to use the input to change the time delay 
between each increment of the Servo position. */
      Delay=input*-1;
      Delay=map(Delay, -100, -1, 1, 99);

    }
  
  }
