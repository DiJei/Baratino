#include "Arduino.h"
#include <Servo.h>

#define PWMA 5
#define PWMB 4
#define   DA 0
#define   DB 2
#define TIME 500
#define TIME_r 83

/*
  Delay based on interrupt
*/

Servo gripper;



#define CLAW D0

void start_claw() {
  gripper.attach(CLAW);
  delay(100);
}

void stop_claw() {
  gripper.detach();
  delay(100);
}

void openClaw() {

  gripper.write(90);
  delay(100);

}

void closeClaw() {

  gripper.write(20);
  delay(100);

}

void init_motor() {
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(DA, OUTPUT);
  pinMode(DB, OUTPUT);
  delay(TIME);
  digitalWrite(PWMA, LOW);
  digitalWrite(PWMB, LOW);
  digitalWrite(DA, LOW);
  digitalWrite(DB, LOW);
  delay(TIME);
}

void stop_motor() {
  digitalWrite(PWMA, LOW);
  digitalWrite(PWMB, LOW);
  digitalWrite(DA, LOW);
  digitalWrite(DB, LOW);
}

bool check_ultra() {
  if (get_distance() <= DIST)  {
    stop_motor();
    execute_command(ultrasonic_command);
    return true;
  }
  return false;
}


void reverse(int times) {
  digitalWrite(PWMA, HIGH);
  digitalWrite(PWMB, HIGH);
  digitalWrite(DA, HIGH);
  digitalWrite(DB, HIGH);
  delay(times * TIME);
  stop_motor();
}

void forward(int times) {
  digitalWrite(PWMA, HIGH);
  digitalWrite(PWMB, HIGH);
  digitalWrite(DA, LOW);
  digitalWrite(DB, LOW);

  for (int x = 0; x <= times; x++) {
    delay(TIME);
    if (check_ultra()) {
      stop_motor();
      return;
    }
  }
  stop_motor();
}

void turnRight(int times) {
  digitalWrite(PWMA, HIGH);
  digitalWrite(PWMB, HIGH);
  digitalWrite(DA, HIGH);
  digitalWrite(DB, LOW);

  for (int x = 0; x <= times; x++) {
    delay(TIME_r);
    if (check_ultra()) {
      stop_motor();
      return;
    }
  }

  stop_motor();
}


void turnLeft(int times) {
  digitalWrite(PWMA, HIGH);
  digitalWrite(PWMB, HIGH);
  digitalWrite(DA, LOW);
  digitalWrite(DB, HIGH);

  for (int x = 0; x <= times; x++) {
    delay(TIME_r);
    if (check_ultra()) {
       stop_motor();
      return;
    }  
  }

  stop_motor();
}

