#include <Servo.h>

Servo servo;
int x, y, input=0;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
servo.attach(8);
servo.write(70);
delay (1000);
}

void loop() {


if(input==1){
  for(x=70; x<160;x++){
  servo.write(x);
  serialEvent();
  if(input==0) break;
  delay(2);  
//    y=servo.read();
//  Serial.print("The servo position is = ");
//  Serial.println(y);
  }
  for(x;x>70;x--){
  servo.write(x);
  serialEvent();
  if(input==0) break;
  delay(2); 
//    y=servo.read();
//  Serial.print("The servo position is = ");
//  Serial.println(y);
    }
}

  }

void serialEvent () {
 // Serial.println("HELLOOOOOOO");
    while(Serial.available())
    {
     input=Serial.parseInt();
  Serial.print("Input is ");
  Serial.println(input);
  
    }
  
  }
