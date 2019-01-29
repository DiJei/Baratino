#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#define trigPin   D7
#define echoPin   D8
#define DIST 10

/*----UDP Server setting----*/
WiFiUDP Udp;
#define PORT  333
int len = 0;
char incomingPacket[255];
char ultrasonic_command[255];
char infrared_command[255];
char replyPacket[] = "ok";
unsigned int packetSize = 0;
unsigned int devices = 0;
/*--------------------------*/
float current_dist = 11.0;


void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT );
  pinMode(D5, OUTPUT);
  pinMode(D6, OUTPUT);
  delay(500);
  digitalWrite(D5, LOW);
  digitalWrite(D6, LOW);
  delay(500);
  /*AP  configuration*/
  boolean result = WiFi.softAP("Baratino");
  IPAddress myIP = WiFi.softAPIP();
  if (result == true)
  {
    play_ready_song();
    delay(500);
    devices = WiFi.softAPgetStationNum();
    await_client();
    Udp.begin(PORT);
  }
  else
  {
    while (1) {
      delay(3000);
    }
  }
  /*----------------*/
  delay(500);
  init_motor();
  delay(500);
  start_claw();
  delay(500);
  closeClaw();
  delay(1000);
  openClaw();
  delay(1000);
  /*----------------*/
}

void loop() {
  //Get from buffer
  packetSize = Udp.parsePacket();
  //Check if something
  if (packetSize) {
    len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    if (incomingPacket[0] == 'S') {
      switch (incomingPacket[1]) {
        case '1':
          copy_command(incomingPacket, ultrasonic_command, len);
          break;
        case '2':
          copy_command(incomingPacket, infrared_command, len);
          break;
        default:
          break;
      }
    }
    else
      execute_command(incomingPacket);
  }
  devices = WiFi.softAPgetStationNum();
  if (devices == 0)
    await_client();
  else
    current_dist = get_distance();


  if (current_dist <= DIST )
    execute_command(ultrasonic_command);
  delay(15);

}
