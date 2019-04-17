#include <Servo.h>

Servo servo;
int x=70, y, d=100, input=1;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
servo.attach(8);
servo.write(70);
delay (1000);
}

void loop() {


if(input!=0){
  while(x<160){
    x=x+input;
    servo.write(x);
    serialEvent();
    if(input==0) break;
    delay(10);  
  }
  while(x>70){
    x=x-input;
    servo.write(x);
    serialEvent();
    if(input==0) break;
    delay(10); 
    }
}

  }

void serialEvent () {
    if(Serial.available()>0)
    {
      input=Serial.parseInt();
      input=input/10;
      Serial.print("Input is ");
      Serial.println(input);


    }
  
  }
