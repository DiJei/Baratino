#include "Arduino.h"

#define trigPin   D7
#define echoPin   D8
#define THERESHOLD   500
#define INFRARED A0


long get_distance() {

  long duration, cm, temp;
  cm = 0;
  temp = 0;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);

  cm = duration * 0.034 / 2;


  return cm;
}

bool get_infrared() {
  if (analogRead(A0) > 200)
    return true;
  return false;
}


