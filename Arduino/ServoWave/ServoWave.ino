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
  for(x; x<160;x++){
    servo.write(x);
    serialEvent();
    if(input==0) break;
    delay(d);  
  }
  for(x;x>70;x--){
  servo.write(x);
  serialEvent();
  if(input==0) break;
  delay(d); 
    }
}

  }

void serialEvent () {
    if(Serial.available()>0)
    {
      input=Serial.parseInt();
      Serial.print("Input is ");
      Serial.println(input);

      d=input*-1;
      d=map(d, -100, -1, 1, 99);
      Serial.print("d is "); Serial.println(d);

    }
  
  }
