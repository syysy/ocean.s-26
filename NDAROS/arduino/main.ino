#include <FastLED.h>

#define RIVER 13
#define RIVER_NUM_LEDS 20
#define OCEAN 12
#define OCEAN_NUM_LEDS 20
#define PIPE_RIVER 11
#define PIPE_RIVER_NUM_LEDS 20
#define PIPE_OCEAN 10
#define PIPE_OCEAN_NUM_LEDS 20

#define PIPE_RIVER_BUTTON 8
#define PIPE_OCEAN_BUTTON 9

#define PIPE_CENTRAL_LEDS 14

#define PIPE_CAPTEUR_AIMANT_1 2
#define PIPE_CAPTEUR_AIMANT_2 3
#define PIPE_CAPTEUR_AIMANT_3 4
#define PIPE_CAPTEUR_AIMANT_4 5
#define PIPE_CAPTEUR_AIMANT_5 6

#define PIPE_CAPTEUR_PRESENCE 7

// OCEAN COLORS
#define OCEAN_COLOR CRGB::Red
#define OCEAN_HIGHLIGHT CRGB(255, 255, 255)
#define OCEAN_COLOR_FINAL CRGB(77, 255, 255)

// RIVER COLORS
#define RIVER_COLOR CRGB::Red
#define RIVER_HIGHLIGHT CRGB(255, 255, 255)
#define RIVER_COLOR_FINAL CRGB(0, 42, 255)


CRGB river_leds[RIVER_NUM_LEDS];
CRGB ocean_leds[OCEAN_NUM_LEDS];
CRGB pipe_river_leds[PIPE_RIVER_NUM_LEDS];
CRGB pipe_ocean_leds[PIPE_OCEAN_NUM_LEDS];
String inputBuffer = "";

void pipeRiver() {
  for (unsigned i = 0; i < PIPE_RIVER_NUM_LEDS; i++) {
    pipe_river_leds[i] = RIVER_COLOR;
    FastLED.show();
  }
  while (1) {
    fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, RIVER_COLOR);

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % PIPE_RIVER_NUM_LEDS;
    pipe_river_leds[firstOffset] = RIVER_HIGHLIGHT;
    FastLED.show();
    delay(150);
  }
}

void pipeOcean() {
  for (unsigned i = 0; i < PIPE_RIVER_NUM_LEDS; i++) {
    pipe_river_leds[i] = OCEAN_COLOR;
    FastLED.show();
  }
  while (1) {
    fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, OCEAN_COLOR);

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % PIPE_OCEAN_NUM_LEDS;
    pipe_ocean_leds[firstOffset] = OCEAN_HIGHLIGHT;
    FastLED.show();
    delay(150);
  }
}

void pipeRiverFinal() {
  for (unsigned i = 0; i < PIPE_RIVER_NUM_LEDS; i++) {
    pipe_river_leds[i] = RIVER_COLOR_FINAL;
    FastLED.show();
  }
  while (1) {
    fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, RIVER_COLOR_FINAL);

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % PIPE_RIVER_NUM_LEDS;
    pipe_river_leds[firstOffset] = RIVER_HIGHLIGHT;
    FastLED.show();
    delay(150);
  }
}

void pipeOceanFinal() {
  for (unsigned i = 0; i < PIPE_RIVER_NUM_LEDS; i++) {
    pipe_river_leds[i] = OCEAN_COLOR_FINAL;
    FastLED.show();
  }
  while (1) {
    fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, OCEAN_COLOR_FINAL);

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % PIPE_OCEAN_NUM_LEDS;
    pipe_ocean_leds[firstOffset] = OCEAN_HIGHLIGHT;
    FastLED.show();
    delay(150);
  }
}

void riverLed() {
  fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR);
  FastLED.show();
}

void oceanLed() {
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR);
  FastLED.show();
}

void riverLedFinal() {
  fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR_FINAL);
  FastLED.show();
}

void oceanLedFinal() {
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR_FINAL);
  FastLED.show();
}

int compteurAimants() {
  int compteur = 0;

  if (digitalRead(PIPE_CAPTEUR_AIMANT_1) == LOW) compteur++;
  if (digitalRead(PIPE_CAPTEUR_AIMANT_2) == LOW) compteur++;
  if (digitalRead(PIPE_CAPTEUR_AIMANT_3) == LOW) compteur++;
  if (digitalRead(PIPE_CAPTEUR_AIMANT_4) == LOW) compteur++;
  if (digitalRead(PIPE_CAPTEUR_AIMANT_5) == LOW) compteur++;

  return compteur;
}

bool presenceDetected() {
  return digitalRead(PIPE_CAPTEUR_PRESENCE) == HIGH;
}

bool isPipeRiverButtonPressed() {
  return digitalRead(PIPE_RIVER_BUTTON) == LOW;
}

bool isPipeOceanButtonPressed() {
  return digitalRead(PIPE_OCEAN_BUTTON) == LOW;
}


void setup() {
  Serial.begin(9600);

  FastLED.addLeds<WS2812B, RIVER, GRB>(river_leds, RIVER_NUM_LEDS);
  FastLED.addLeds<WS2812B, OCEAN, GRB>(ocean_leds, OCEAN_NUM_LEDS);
  FastLED.setBrightness(255);
  
  fill_solid(river_leds, RIVER_NUM_LEDS, CRGB::Black);
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, CRGB::Black);
  fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, CRGB::Black);
  fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, CRGB::Black);
  FastLED.show();

  pinMode(PIPE_CAPTEUR_AIMANT_1, INPUT_PULLUP);
  pinMode(PIPE_CAPTEUR_AIMANT_2, INPUT_PULLUP);
  pinMode(PIPE_CAPTEUR_AIMANT_3, INPUT_PULLUP);
  pinMode(PIPE_CAPTEUR_AIMANT_4, INPUT_PULLUP);
  pinMode(PIPE_CAPTEUR_AIMANT_5, INPUT_PULLUP);

  pinMode(PIPE_CAPTEUR_PRESENCE, INPUT_PULLUP);

  pinMode(PIPE_RIVER_BUTTON, INPUT_PULLUP);
  pinMode(PIPE_OCEAN_BUTTON, INPUT_PULLUP);

  delay(1000);
}

void loop() {
  FastLED.show();


  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer == "SEPARATION") {
        riverLedFinal();
        oceanLedFinal();
        pipeRiverFinal();
        pipeOceanFinal();
      } else if (inputBuffer == "CAPTEUR_AIMANT") {
        int count = compteurAimants();
        Serial.println(count);
      } else if (inputBuffer == "PIPE_OCEAN") {
        pipeOcean();
      } else if (inputBuffer == "PIPE_RIVER") {
        pipeRiver();
      } else if (inputBuffer == "PRESENCE") {
        if (presenceDetected()) {
          Serial.println("PRESENCE");
        }
      } else if (inputBuffer == "OCEAN_RIVER") {
        oceanLed();
      } else if (inputBuffer == "PIPE_AVAILABLE") {
        if (isPipeRiverButtonPressed()) {
          Serial.println("BUTTON_RIVER_PRESSED");
        }
        if (isPipeOceanButtonPressed()) {
          Serial.println("BUTTON_OCEAN_PRESSED");
        }
      }
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }
}