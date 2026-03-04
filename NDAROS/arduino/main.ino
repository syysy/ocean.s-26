#include <FastLED.h>


#define RIVER 13
#define RIVER_NUM_LEDS 20
#define OCEAN 12
#define OCEAN_NUM_LEDS 20
const int pinBouton = 8;

const int pinCapteurAimant1 = 2;
const int pinCapteurAimant2 = 3;
const int pinCapteurAimant3 = 4;


CRGB river_leds[RIVER_NUM_LEDS];
CRGB ocean_leds[OCEAN_NUM_LEDS];
String inputBuffer = "";

/*void pipeRiver() {
  for (unsigned int i = 0; i < 10000; i++) {
    fill_solid(leds, RIVER_NUM_LEDS, CRGB(0,42,255));

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % RIVER_NUM_LEDS;
    river_leds[firstOffset] = CRGB(77,255,255);
    FastLED.show();
    delay(150);
  }
}

void pipeOcean() {
  for (unsigned int i = 0; i < 10000; i++) {
    fill_solid(leds, NUM_LEDS, CRGB(77,255,255));

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % NUM_LEDS;
    ocean_leds[firstOffset] = CRGB(255,255,255);
    FastLED.show();
    delay(150);
  }
}*/

void riverLedInit() {
  fill_solid(river_leds, RIVER_NUM_LEDS, CRGB(255,255,255));
  FastLED.show();
}

void oceanLedInit() {
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, CRGB(255,255,255));
  FastLED.show();
}

void riverLedFinal() {
  fill_solid(river_leds, RIVER_NUM_LEDS, CRGB::Red);
  FastLED.show();
}

void oceanLedFinal() {
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, CRGB::Red);
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
  
  riverLedInit();
  oceanLedInit();

  pinMode(pinCapteurAimant1, INPUT_PULLUP);
  pinMode(pinCapteurAimant2, INPUT_PULLUP);
  pinMode(pinCapteurAimant3, INPUT_PULLUP);

  pinMode(pinBouton, INPUT_PULLUP); 

  delay(1000);
}

void loop() {
  FastLED.show();

  delay(2000);
  

  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer == "SEPARATION") {
        riverLedFinal();
        oceanLedFinal();
      } else if (inputBuffer == "compteurAimants") {
        int count = compteurAimants();
        Serial.println(count);
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