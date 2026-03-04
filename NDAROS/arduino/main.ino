#include <FastLED.h>


#define LED_PIN 13
#define NUM_LEDS 26
const int pinBouton = 8;


CRGB leds[NUM_LEDS];
String inputBuffer = "";


void setup() {
 Serial.begin(9600);
 FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
 FastLED.setBrightness(255);
 fill_solid(leds, NUM_LEDS, CRGB::Black);
 FastLED.show();


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