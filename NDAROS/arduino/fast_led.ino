#include <FastLED.h>


#define LED_PIN 13
#define NUM_LEDS 26


CRGB leds[NUM_LEDS];


void setup() {
 FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
 FastLED.setBrightness(255);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
 FastLED.show();
 for (int i = 0; i < NUM_LEDS; i++) {
   leds[i] = CRGB(0,42,255);
   FastLED.show();
   delay(150);
 }
}


void loop() {
 // fill_solid(leds, NUM_LEDS, CRGB(102,255,255));
 fill_solid(leds, NUM_LEDS, CRGB(0,42,255));


 static int firstOffset = 0;
 firstOffset = (firstOffset + 1) % NUM_LEDS;
  leds[firstOffset] = CRGB(77,255,255);


 FastLED.show();
 delay(150);
}
