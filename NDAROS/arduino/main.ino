#include <Adafruit_NeoPixel.h>
#include <math.h>

#define RIVER 13
#define RIVER_NUM_LEDS 100
#define OCEAN 12
#define OCEAN_NUM_LEDS 100
#define PIPE_RIVER 11
#define PIPE_RIVER_NUM_LEDS 50
#define PIPE_OCEAN 10
#define PIPE_OCEAN_NUM_LEDS 50

#define RIVER_BUTTON 8
#define OCEAN_BUTTON 9

#define CENTRAL_BUTTON 22
#define CENTRAL_LEDS 23
#define CENTRAL_NUM_LEDS 24

#define CITY_LED 24
#define CITY_NUM_LEDS 71

// NeoPixel strips
Adafruit_NeoPixel river_strip = Adafruit_NeoPixel(RIVER_NUM_LEDS, RIVER, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel ocean_strip = Adafruit_NeoPixel(OCEAN_NUM_LEDS, OCEAN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pipe_river_strip = Adafruit_NeoPixel(PIPE_RIVER_NUM_LEDS, PIPE_RIVER, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pipe_ocean_strip = Adafruit_NeoPixel(PIPE_OCEAN_NUM_LEDS, PIPE_OCEAN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel central_led = Adafruit_NeoPixel(CENTRAL_NUM_LEDS, CENTRAL_LEDS, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel city_leds(CITY_NUM_LEDS, CITY_LED, NEO_GRB + NEO_KHZ800);
const int city_full_led_indices[] = {0, 3, 7, 10, 18, 25, 29, 31, 38, 50, 55, 60, 65, 70};
const int nbIndicesFull = sizeof(city_full_led_indices) / sizeof(city_full_led_indices[0]);

float centralOffset = 0.0; 
bool isCentralAnimActive = false;
bool cityLedOn = false;
bool cityLedBlack = false;
bool waitingForCentralButton = false;

#define MAGNET_SENSOR_1 2
#define MAGNET_SENSOR_2 3
#define MAGNET_SENSOR_3 4

#define PRESENCE_SENSOR 7

// OCEAN COLORS (as 32-bit packed color: Color(R, G, B))
#define OCEAN_COLOR ocean_strip.Color(70, 150, 215)
#define OCEAN_COLOR_1 ocean_strip.Color(59, 135, 202)
#define OCEAN_COLOR_2 ocean_strip.Color(36, 104, 177)
#define OCEAN_COLOR_FINAL ocean_strip.Color(14, 73, 151)

// RIVER COLORS
#define RIVER_COLOR river_strip.Color(70, 150, 215)
#define RIVER_COLOR_1 river_strip.Color(66, 154, 204)
#define RIVER_COLOR_2 river_strip.Color(59, 163, 183)
#define RIVER_COLOR_FINAL river_strip.Color(52, 172, 161)

String inputBuffer = "";

// Non-blocking pipe animation state
bool pipeRiverActive = false;
bool pipeOceanActive = false;
unsigned int pipeRiverIndex = 0;
unsigned int pipeOceanIndex = 0;
unsigned long pipeRiverLastUpdate = 0;
unsigned long pipeOceanLastUpdate = 0;
const unsigned long PIPE_DELAY = 100;

// Helper function to show all strips
void showAllStrips() {
  river_strip.show();
  ocean_strip.show();
  pipe_river_strip.show();
  pipe_ocean_strip.show();
}

void initLeds() {
  river_strip.fill(river_strip.Color(255, 0, 0));
  ocean_strip.fill(ocean_strip.Color(255, 0, 0));
  pipe_river_strip.fill(pipe_river_strip.Color(255, 0, 0));
  pipe_ocean_strip.fill(pipe_ocean_strip.Color(255, 0, 0));
  central_led.fill(central_led.Color(255, 0, 0));
  city_leds.fill(city_leds.Color(255, 0, 0));
  showAllStrips();
}

void resetPipes() {
  pipe_river_strip.fill(0);
  pipe_ocean_strip.fill(0);
  pipe_river_strip.show();
  pipe_ocean_strip.show();
  showAllStrips();
}

void pipeRiver() {
  pipeRiverActive = true;
  pipeRiverIndex = 0;
  pipeRiverLastUpdate = millis();
}

void pipeOcean() {
  pipeOceanActive = true;
  pipeOceanIndex = 0;
  pipeOceanLastUpdate = millis();
}

void updatePipeAnimations() {
  unsigned long now = millis();
  
  if (pipeRiverActive && (now - pipeRiverLastUpdate >= PIPE_DELAY)) {
    if (pipeRiverIndex < PIPE_RIVER_NUM_LEDS) {
      pipe_river_strip.setPixelColor(pipeRiverIndex, RIVER_COLOR);
      pipe_river_strip.show();
      pipeRiverIndex++;
      pipeRiverLastUpdate = now;
    } else {
      pipeRiverActive = false;
    }
  }
  
  if (pipeOceanActive && (now - pipeOceanLastUpdate >= PIPE_DELAY)) {
    if (pipeOceanIndex < PIPE_OCEAN_NUM_LEDS) {
      pipe_ocean_strip.setPixelColor(pipeOceanIndex, OCEAN_COLOR);
      pipe_ocean_strip.show();
      pipeOceanIndex++;
      pipeOceanLastUpdate = now;
    } else {
      pipeOceanActive = false;
    }
  }
}

void oceanRiverLed() {
  river_strip.fill(RIVER_COLOR);
  ocean_strip.fill(OCEAN_COLOR); 
  river_strip.show();
  ocean_strip.show();
}

void mangroveLed1() {
  pipe_river_strip.fill(RIVER_COLOR_1);
  pipe_ocean_strip.fill(OCEAN_COLOR_1);
  river_strip.fill(RIVER_COLOR_1);
  ocean_strip.fill(OCEAN_COLOR_1);
  showAllStrips();
}

void mangroveLed2() {
  pipe_river_strip.fill(RIVER_COLOR_2);
  pipe_ocean_strip.fill(OCEAN_COLOR_2);
  river_strip.fill(RIVER_COLOR_2);
  ocean_strip.fill(OCEAN_COLOR_2);
  showAllStrips();
}

void mangroveLed3() {
  pipe_river_strip.fill(RIVER_COLOR_FINAL);
  pipe_ocean_strip.fill(OCEAN_COLOR_FINAL);
  river_strip.fill(RIVER_COLOR_FINAL);
  ocean_strip.fill(OCEAN_COLOR_FINAL);
  showAllStrips();
}

int compteurAimants() {
  int compteur = 0;

  if (digitalRead(MAGNET_SENSOR_1) == LOW) compteur++;
  if (digitalRead(MAGNET_SENSOR_2) == LOW) compteur++;
  if (digitalRead(MAGNET_SENSOR_3) == LOW) compteur++;

  return compteur;
}

bool presenceDetected() {
  return digitalRead(PRESENCE_SENSOR) == HIGH;
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

void centralYellowAnimation() {
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

void centrelWhiteAnimation() {
  central_led.clear();
  for(int i = 0; i < CENTRAL_NUM_LEDS; i++) {
    float position = (float)i / CENTRAL_NUM_LEDS; 
    float onde = sin( (position * 6.28) + centralOffset ); 
    float intensite = pow((onde + 1.0) / 2.0, 2); 

    central_led.setPixelColor(i, central_led.Color((int)(255 * intensite), (int)(255 * intensite), (int)(255 * intensite)));
  }
  central_led.show();
  centralOffset -= 0.1; 
}

void centralRedAnimation() {
  central_led.clear();
  central_led.fill(central_led.Color(255, 0, 0));
  central_led.show();
}

void centralOffAnimation() {
  central_led.clear();
  central_led.show();
}

void cityLedOnRed() {
  city_leds.clear();
  for (int i = 0; i < nbIndicesFull; i++) {
    int ledIndex = city_full_led_indices[i];
    if (ledIndex < CITY_NUM_LEDS) {
      city_leds.setPixelColor(ledIndex, city_leds.Color(255, 0, 0)); 
    }
  }
  city_leds.show();  
}

void UpdateCityLed(int aimants) {
  city_leds.clear(); 

  if (aimants > 0) {
    int cleanAimants = constrain(aimants, 1, 3);
    int intensity = 0;

    if (cleanAimants == 1) intensity = 30; 
    if (cleanAimants == 2) intensity = 110;
    if (cleanAimants == 3) intensity = 255;

    for (int i = 0; i < nbIndicesFull; i++) {
      int ledIndex = city_full_led_indices[i];
      if (ledIndex < CITY_NUM_LEDS) {
        city_leds.setPixelColor(ledIndex, city_leds.Color(intensity, intensity, intensity));
      }
    }
  } 
  else {
    // Cas 0 aimants : Faible intensité, une sur deux
    int lowIntensity = 8; 
    for (int i = 0; i < nbIndicesFull; i += 2) { 
      int ledIndex = city_full_led_indices[i];
      if (ledIndex < CITY_NUM_LEDS) {
        city_leds.setPixelColor(ledIndex, city_leds.Color(lowIntensity, lowIntensity, lowIntensity));
      }
    }
  }

  city_leds.show();
}

void cityLedOff() {
  city_leds.clear();
  city_leds.show();
}

void setup() {
  Serial.begin(9600);

  // Initialize all NeoPixel strips
  river_strip.begin();
  ocean_strip.begin();
  pipe_river_strip.begin();
  pipe_ocean_strip.begin();
  central_led.begin();
  city_leds.begin();
  
  river_strip.setBrightness(255);
  ocean_strip.setBrightness(255);
  pipe_river_strip.setBrightness(255);
  pipe_ocean_strip.setBrightness(255);
  central_led.setBrightness(50);
  city_leds.setBrightness(255); 

  pinMode(MAGNET_SENSOR_1, INPUT_PULLUP);
  pinMode(MAGNET_SENSOR_2, INPUT_PULLUP);
  pinMode(MAGNET_SENSOR_3, INPUT_PULLUP);

  pinMode(PRESENCE_SENSOR, INPUT_PULLUP);
  pinMode(CENTRAL_BUTTON, INPUT_PULLUP);

  pinMode(RIVER_BUTTON, INPUT_PULLUP);
  pinMode(OCEAN_BUTTON, INPUT_PULLUP);

  delay(1000);
}

void loop() {
  // Update non-blocking pipe animations
  updatePipeAnimations();
  
  if (waitingForCentralButton) {
    centralYellowAnimation();
    if (isPipeCentralButtonPressed()) {
      waitingForCentralButton = false;
      cityLedOn = true;
      Serial.println("BUTTON_CENTRAL_PRESSED");
      UpdateCityLed(compteurAimants());
    }
  } else if (cityLedOn) {
    centrelWhiteAnimation();
  } else if (cityLedBlack) {
    centralOffAnimation();
    cityLedOff();
  } else {
    centralRedAnimation();
    cityLedOnRed();
  }

  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer == "SEPARATION") {
        int aimants = compteurAimants();
        UpdateCityLed(aimants);
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
          cityLedOff();
          cityLedBlack = true;
        }
      } else if (inputBuffer == "OCEAN_RIVER") {
        oceanRiverLed();
		    resetPipes();
        cityLedBlack = true;
        cityLedOn = false;
      } else if (inputBuffer == "PIPE_AVAILABLE") {
        if (isPipeRiverButtonPressed()) {
          Serial.println("BUTTON_RIVER_PRESSED");
        }
        if (isPipeOceanButtonPressed()) {
          Serial.println("BUTTON_OCEAN_PRESSED");
        }
      } else if (inputBuffer == "BUTTON_CENTRAL") {
        waitingForCentralButton = true; 
        cityLedBlack = false;
        cityLedOn = false;
      } else if (inputBuffer == "RESET") {
        initLeds();
        waitingForCentralButton = false;
        cityLedOn = false;
        cityLedBlack = false;
      }
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }
}