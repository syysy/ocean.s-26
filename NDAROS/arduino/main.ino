#include <FastLED.h>


#define LED_PIN 13
#define NUM_LEDS 26
const int pinBouton = 8;

const int pinCapteurAimant1 = 2;
const int pinCapteurAimant2 = 3;
const int pinCapteurAimant3 = 4;


CRGB leds[NUM_LEDS];
String inputBuffer = "";


void setup() {
 Serial.begin(9600);
 FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
 FastLED.setBrightness(255);
 fill_solid(leds, NUM_LEDS, CRGB::Black);
 FastLED.show();

  pinMode(pinCapteurAimant1, INPUT_PULLUP);
  pinMode(pinCapteurAimant2, INPUT_PULLUP);
  pinMode(pinCapteurAimant3, INPUT_PULLUP);

 pinMode(pinBouton, INPUT_PULLUP); 

 delay(1000);
}


void led() {
  for (unsigned int i = 0; i < 10000; i++) {
    fill_solid(leds, NUM_LEDS, CRGB(0,42,255));

    static int firstOffset = 0;
    firstOffset = (firstOffset + 1) % NUM_LEDS;
    leds[firstOffset] = CRGB(77,255,255);
    FastLED.show();
    delay(150);
  }
}

// Fonction pour compter le nombre de capteurs d'aimant activés
int nb_aimant() {
  int compteur = 0;

  if (digitalRead(pinCapteurAimant1) == LOW) compteur++;
  if (digitalRead(pinCapteurAimant2) == LOW) compteur++;
  if (digitalRead(pinCapteurAimant3) == LOW) compteur++;

  return compteur;
}

void loop() {
  FastLED.show();

  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer == "LED") {
        led();
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