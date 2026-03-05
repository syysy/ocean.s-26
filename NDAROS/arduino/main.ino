#include <FastLED.h>
#include <Adafruit_NeoPixel.h>
#include <math.h>

#define RIVER 13
#define RIVER_NUM_LEDS 20
#define OCEAN 12
#define OCEAN_NUM_LEDS 20
#define PIPE_RIVER 11
#define PIPE_RIVER_NUM_LEDS 50
#define PIPE_OCEAN 10
#define PIPE_OCEAN_NUM_LEDS 50

#define RIVER_BUTTON 8
#define OCEAN_BUTTON 9

#define CENTRAL_LEDS 23
#define CENTRAL_BUTTON 22
#define CENTRAL_NUM_LEDS 24

Adafruit_NeoPixel central_led = Adafruit_NeoPixel(CENTRAL_NUM_LEDS, CENTRAL_LEDS, NEO_GRB + NEO_KHZ800);
float centralOffset = 0.0; 
bool isCentralAnimActive = false;
bool isCentralButtonClicked = false;

#define CAPTEUR_AIMANT_1 2
#define CAPTEUR_AIMANT_2 3
#define CAPTEUR_AIMANT_3 4
#define CAPTEUR_AIMANT_4 5
#define CAPTEUR_AIMANT_5 6

#define CAPTEUR_PRESENCE 7

// OCEAN COLORS
#define OCEAN_COLOR CRGB(70, 150, 215)
#define OCEAN_HIGHLIGHT CRGB(255, 255, 255)
#define OCEAN_COLOR_1 CRGB(59, 135, 202)
#define OCEAN_COLOR_2 CRGB(36, 104, 177)
#define OCEAN_COLOR_FINAL CRGB(14, 73, 151)

// RIVER COLORS
#define RIVER_COLOR CRGB(70, 150, 215)
#define RIVER_HIGHLIGHT CRGB(255, 255, 255)
#define RIVER_COLOR_1 CRGB(66, 154, 204)
#define RIVER_COLOR_2 CRGB(59, 163, 183)
#define RIVER_COLOR_FINAL CRGB(52, 172, 161)


CRGB river_leds[RIVER_NUM_LEDS];
CRGB ocean_leds[OCEAN_NUM_LEDS];
CRGB pipe_river_leds[PIPE_RIVER_NUM_LEDS];
CRGB pipe_ocean_leds[PIPE_OCEAN_NUM_LEDS];
String inputBuffer = "";

void initLeds() {
  fill_solid(river_leds, RIVER_NUM_LEDS, CRGB::Red);
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, CRGB::Red);
  fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, CRGB::Red);
  fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, CRGB::Red);
  FastLED.show();
}

void resetPipes() {
  fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, CRGB::Black);
  fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void pipeRiver() {
  for (unsigned i = 0; i < PIPE_RIVER_NUM_LEDS; i++) {
    pipe_river_leds[i] = RIVER_COLOR;
    FastLED.show();
	delay(200);
  }
}

void pipeOcean() {
  for (unsigned i = 0; i < PIPE_OCEAN_NUM_LEDS; i++) {
    pipe_ocean_leds[i] = OCEAN_COLOR;
    FastLED.show();
    delay(200);
  }
}

void oceanRiverLed() {
  fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR);
  fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR); 
  FastLED.show();
}

void mangroveLed1() {
	fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, RIVER_COLOR_1);
	fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, OCEAN_COLOR_1);
	fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR_1);
	fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR_1);
	FastLED.show();
}

void mangroveLed2() {
	fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, RIVER_COLOR_2);
	fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, OCEAN_COLOR_2);
	fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR_2);
	fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR_2);
	FastLED.show();
}

void mangroveLed3() {
	fill_solid(pipe_river_leds, PIPE_RIVER_NUM_LEDS, RIVER_COLOR_FINAL);
	fill_solid(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS, OCEAN_COLOR_FINAL);
	fill_solid(river_leds, RIVER_NUM_LEDS, RIVER_COLOR_FINAL);
	fill_solid(ocean_leds, OCEAN_NUM_LEDS, OCEAN_COLOR_FINAL);
	FastLED.show();
}

int compteurAimants() {
  int compteur = 0;

  if (digitalRead(CAPTEUR_AIMANT_1) == LOW) compteur++;
  if (digitalRead(CAPTEUR_AIMANT_2) == LOW) compteur++;
  if (digitalRead(CAPTEUR_AIMANT_3) == LOW) compteur++;
  if (digitalRead(CAPTEUR_AIMANT_4) == LOW) compteur++;
  if (digitalRead(CAPTEUR_AIMANT_5) == LOW) compteur++;

  return compteur;
}

bool presenceDetected() {
  return digitalRead(CAPTEUR_PRESENCE) == HIGH;
}

bool isPipeRiverButtonPressed() {
  return digitalRead(RIVER_BUTTON) == LOW;
}

bool isPipeOceanButtonPressed() {
  return digitalRead(OCEAN_BUTTON) == LOW;
}

bool isPipeCentralButtonPressed() {
  return digitalRead(CENTRAL_BUTTON) == LOW;
}

void runCentralAnimation() {
  central_led.clear();
  for(int i = 0; i < CENTRAL_NUM_LEDS; i++) {
    float position = (float)i / CENTRAL_NUM_LEDS; 
    float onde = sin( (position * 6.28) + centralOffset ); 
    float intensite = pow((onde + 1.0) / 2.0, 2); 

    central_led.setPixelColor(i, central_led.Color((int)(255 * intensite), (int)(180 * intensite), 0));
  }
  central_led.show();
  centralOffset -= 0.1; 
}

void centralAnimation() {
  central_led.clear();
  central_led.fill(CRGB::White);
  central_led.show();
}

void centralRedAnimation() {
  central_led.clear();
  central_led.fill(CRGB::Red);
  central_led.show();
}

void centralOffAnimation() {
  central_led.clear();
  central_led.show();
}


void setup() {
  Serial.begin(9600);

  FastLED.addLeds<WS2812B, RIVER, GRB>(river_leds, RIVER_NUM_LEDS);
  FastLED.addLeds<WS2812B, OCEAN, GRB>(ocean_leds, OCEAN_NUM_LEDS);
  FastLED.addLeds<WS2812B, PIPE_RIVER, GRB>(pipe_river_leds, PIPE_RIVER_NUM_LEDS);
  FastLED.addLeds<WS2812B, PIPE_OCEAN, GRB>(pipe_ocean_leds, PIPE_OCEAN_NUM_LEDS);
  FastLED.setBrightness(255);
  
  pinMode(CAPTEUR_AIMANT_1, INPUT_PULLUP);
  pinMode(CAPTEUR_AIMANT_2, INPUT_PULLUP);
  pinMode(CAPTEUR_AIMANT_3, INPUT_PULLUP);
  pinMode(CAPTEUR_AIMANT_4, INPUT_PULLUP);
  pinMode(CAPTEUR_AIMANT_5, INPUT_PULLUP);

  pinMode(CAPTEUR_PRESENCE, INPUT_PULLUP);
  pinMode(CENTRAL_BUTTON, INPUT_PULLUP);

  pinMode(RIVER_BUTTON, INPUT_PULLUP);
  pinMode(OCEAN_BUTTON, INPUT_PULLUP);

  central_led.begin();
  central_led.setBrightness(50);

  delay(1000);
}

void loop() {
  FastLED.show();
  if (isCentralAnimActive) {
    runCentralAnimation();
  }

  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer == "SEPARATION") {
        int aimants = compteurAimants();
        if (aimants == 1) {
            mangroveLed1();
        } else if (aimants == 2) {
            mangroveLed2();
        } else if (aimants == 3) {
            mangroveLed3();
        }
      } else if (inputBuffer == "MAGNET_COUNTER") {
        int count = compteurAimants();
        Serial.println(count);
      } else if (inputBuffer == "PIPE_OCEAN") {
        pipeOcean();
      } else if (inputBuffer == "PIPE_RIVER") {
        pipeRiver();
      } else if (inputBuffer == "PRESENCE") {
        if (presenceDetected()) {
          Serial.println("PRESENCE");
          centralOffAnimation();
        }
      } else if (inputBuffer == "OCEAN_RIVER") {
        oceanRiverLed();
		resetPipes();
      } else if (inputBuffer == "PIPE_AVAILABLE") {
        if (isPipeRiverButtonPressed()) {
          Serial.println("BUTTON_RIVER_PRESSED");
        }
        if (isPipeOceanButtonPressed()) {
          Serial.println("BUTTON_OCEAN_PRESSED");
        }
      } else if (inputBuffer == "BUTTON_CENTRAL") {
        isCentralAnimActive = true;
        while (!isPipeCentralButtonPressed()) {
            delay(50);
            runCentralAnimation();
            FastLED.show();
        }
        isCentralButtonClicked = true;
        Serial.println("BUTTON_CENTRAL_PRESSED");
        centralAnimation();
        isCentralAnimActive = false;
        delay(500);
	  } else if (inputBuffer == "RESET") {
        initLeds();
		    centralOffAnimation();
		    centralRedAnimation();
      }
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }
}