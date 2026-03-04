#include <FastLED.h>

#define RIVER 13
#define RIVER_NUM_LEDS 20
#define OCEAN 12
#define OCEAN_NUM_LEDS 20
#define PIPE_RIVER 8
#define PIPE_RIVER_NUM_LEDS 20
#define PIPE_OCEAN 7
#define PIPE_OCEAN_NUM_LEDS 20

// OCEAN COLORS
#define OCEAN_COLOR CRGB::Red
#define OCEAN_HIGHLIGHT CRGB(255, 255, 255)
#define OCEAN_COLOR_FINAL CRGB(77, 255, 255)

// RIVER COLORS
#define RIVER_COLOR CRGB::Red
#define RIVER_HIGHLIGHT CRGB(255, 255, 255)
#define RIVER_COLOR_FINAL CRGB(0, 42, 255)

const int pinBouton = 8;

const int pinCapteurAimant1 = 2;
const int pinCapteurAimant2 = 3;
const int pinCapteurAimant3 = 4;


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

  if (digitalRead(pinCapteurAimant1) == LOW) compteur++;
  if (digitalRead(pinCapteurAimant2) == LOW) compteur++;
  if (digitalRead(pinCapteurAimant3) == LOW) compteur++;

  return compteur;
}

void setup() {
  Serial.begin(9600);

  FastLED.addLeds<WS2812B, RIVER, GRB>(river_leds, RIVER_NUM_LEDS);
  FastLED.addLeds<WS2812B, OCEAN, GRB>(ocean_leds, OCEAN_NUM_LEDS);
  FastLED.setBrightness(255);
  
  fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR);
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR);
  fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, CRGB::Black);
  fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, CRGB::Black);
  FastLED.show();

  pinMode(pinCapteurAimant1, INPUT_PULLUP);
  pinMode(pinCapteurAimant2, INPUT_PULLUP);
  pinMode(pinCapteurAimant3, INPUT_PULLUP);

  pinMode(pinBouton, INPUT_PULLUP); 

  delay(1000);
}

void loop() {
  FastLED.show();

  delay(2000);
  riverLedFinal();
  oceanLedFinal();

  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer == "SEPARATION") {
        riverLedFinal();
        oceanLedFinal();
        pipeRiverFinal();
        pipeOceanFinal();
      } else if (inputBuffer == "compteurAimants") {
        int count = compteurAimants();
        Serial.println(count);
      } else if (inputBuffer == "PIPE_OCEAN") {
        pipeOcean();
      } else if (inputBuffer == "PIPE_RIVER") {
        pipeRiver();
      }
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }

  int etatBouton = digitalRead(pinBouton);

  if (etatBouton == LOW) {
    Serial.println("PRESENCE");
  }
}