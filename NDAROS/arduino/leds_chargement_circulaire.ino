#include <Adafruit_NeoPixel.h>
#include <math.h>

#define PIN_COLOR 5
#define NUMPIXELS 24

Adafruit_NeoPixel pixels(NUMPIXELS, PIN_COLOR, NEO_GRB + NEO_KHZ800);

float offset = 0.0; 

float compression = 8.0; 

void setup() {
  pixels.begin();
  pixels.setBrightness(50); 
}

void loop() {
  pixels.clear();

  for(int i = 0; i < NUMPIXELS; i++) {
    float position = (float)i / NUMPIXELS; 
    float onde = sin( (position * 6.28) + offset ); 
    float intensite = (onde + 1.0) / 2.0;     
    intensite = intensite * intensite;

    int r = (int)(255 * intensite); 
    int g = (int)(180 * intensite); 
    int b = 0; 

    pixels.setPixelColor(i, pixels.Color(r, g, b));
  }

  pixels.show();
  offset -= 0.2; // Vitesse de rotation
  delay(20); 
}