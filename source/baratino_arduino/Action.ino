#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494

void execute_command(char *command) {
  int id = 0;
  int times = 0;
  int jump = 0;
  for (int x = 0; command[x] != 0; x++) {
    //Moviment command
    if (command[x] == 'M') {
      if ((command[x + 1] - 48) < 5) {
        if (command[x + 3] - 48 <= 9 && command[x + 3] - 48 >= 0) {
          times = (command[x + 2] - 48) * 10 + (command[x + 3] - 48);
          jump = 3;
        }
        else {
          times = (command[x + 2] - 48);
          jump = 2;
        }
      }
      switch (command[x + 1]) {
        case '1':
          forward(times);
          x = x + jump;
          break;
        case '2':
          reverse(times);
          x = x + jump;
          break;
        case '3':
          turnRight(times);
          x = x + jump;
          break;
        case '4':
          turnLeft(times);
          x = x + jump;
          break;
        case '5':
          openClaw();
          x = x + 1;
          break;
        case '6':
          closeClaw();
          x = x + 1;
          break;
        default:
          break;
      }
    }
    //Audio
    else if (command[x] == 'A') {
      if ((command[x + 1] - 48) < 9) {
        if (command[x + 3] - 48 <= 9 && command[x + 3] - 48 >= 0) {
          times = (command[x + 2] - 48) * 10 + (command[x + 3] - 48);
          jump = 3;
        }
        else {
          times = (command[x + 2] - 48);
          jump = 2;
        }
      }
      switch (command[x + 1]) {
        case '1':
          play_nothing(times);
          x = x + jump;
          break;
        case '2':
          play_note(NOTE_C4, times);
          x = x + jump;
          break;
        case '3':
          play_note(NOTE_D4, times);
          x = x + jump;
          break;
        case '4':
          play_note(NOTE_E4, times);
          x = x + jump;
          break;
        case '5':
          play_note(NOTE_F4, times);
          x = x + jump;
          break;
        case '6':
          play_note(NOTE_G4, times);
          x = x + jump;
          break;
        case '7':
          play_note(NOTE_A4, times);
          x = x + jump;
          break;
        case '8':
          play_note(NOTE_B4, times);
          x = x + jump;
          break;
        default:
          break;
      }
    }
  }
}

void copy_command(char *command, char *sensor_command, int len) {
  int x = 0;
  int y = 0;

  for (x = 2; command[x] != 0; x ++) {
    sensor_command[y] = command[x];
    y++;
  }
  sensor_command[y] = 0;
}

void await_client() {
  while (!devices) {
    digitalWrite(D5, LOW);
    devices = WiFi.softAPgetStationNum();
    delay(500);
    digitalWrite(D5, HIGH);
    delay(500);
  }
  return;
}
