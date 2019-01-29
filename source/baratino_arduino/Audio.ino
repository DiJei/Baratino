#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define TIME     125
#define SOUND_PIN D6

/*Play Note for period of time*/
void play_note(int note, int times) {
  tone(SOUND_PIN, note);
  delay(times * TIME);
  noTone(SOUND_PIN);
  delay(15);
}

/*NO sound*/
void play_nothing(int times) {
  delay(times * TIME);
  noTone(SOUND_PIN);
  delay(15);
}

void play_ready_song() {

  tone(SOUND_PIN, NOTE_C4);
  delay(250);
  noTone(SOUND_PIN);
  delay(50);

  tone(SOUND_PIN, NOTE_D4);
  delay(250);
  noTone(SOUND_PIN);
  delay(50);

  tone(SOUND_PIN, NOTE_E4);
  delay(500);
  noTone(SOUND_PIN);
  delay(50);

  tone(SOUND_PIN, NOTE_F4);
  delay(125);
  noTone(SOUND_PIN);
  delay(25);

  tone(SOUND_PIN, NOTE_F4);
  delay(125);
  noTone(SOUND_PIN);
  delay(25);

  delay(500);
}


