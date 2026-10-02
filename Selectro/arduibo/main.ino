#include <Adafruit_NeoPixel.h>

// Pins
#define LED_PIN 6
#define LED_PIN2 7
#define ATOMIZER_PIN 8
#define BTN_1 3
#define BTN_2 4
#define BTN_ATOM 2

#define LED_COUNT 18
const unsigned long DURATION_MS = 10000;
const unsigned long STEP_MS = 100;

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip2(LED_COUNT, LED_PIN2, NEO_GRB + NEO_KHZ800);

// États
bool led1Active = false, led2Active = false, atomActive = false;
unsigned long startTime = 0;
unsigned long lastStepTime = 0;
int currentStep = 0;

// Debounce simple
bool lastBtn1 = HIGH, lastBtn2 = HIGH, lastBtnAtom = HIGH;

void stopAll() {
  led1Active = false;
  led2Active = false;
  atomActive = false;
  
  strip.clear(); strip.show();
  strip2.clear(); strip2.show();
  digitalWrite(ATOMIZER_PIN, LOW);
  
  // Petit délai pour éviter les rebonds électriques lors de la coupure
  delay(50); 
}

void setup() {
  Serial.begin(9600);
  pinMode(BTN_1, INPUT_PULLUP);
  pinMode(BTN_2, INPUT_PULLUP);
  pinMode(BTN_ATOM, INPUT_PULLUP);
  pinMode(ATOMIZER_PIN, OUTPUT);
  
  strip.begin(); strip.show();
  strip2.begin(); strip2.show();
}

void loop() {
  unsigned long now = millis();

  // Lecture des boutons
  bool b1 = digitalRead(BTN_1);
  bool b2 = digitalRead(BTN_2);
  bool ba = digitalRead(BTN_ATOM);

  // Appui Bouton 1
  if (b1 == LOW && lastBtn1 == HIGH) {
    stopAll();
    Serial.println("LED");
    led1Active = true;
    startTime = now;
    currentStep = 0;
  }
  // Appui Bouton 2
  if (b2 == LOW && lastBtn2 == HIGH) {
    stopAll();
    Serial.println("LED2");
    led2Active = true;
    startTime = now;
    currentStep = 0;
  }
  // Appui Bouton Atomiseur
  if (ba == LOW && lastBtnAtom == HIGH) {
    stopAll();
    Serial.println("ATOM");
    atomActive = true;
    startTime = now;
    digitalWrite(ATOMIZER_PIN, HIGH);
  }

  lastBtn1 = b1; lastBtn2 = b2; lastBtnAtom = ba;

  // --- Animations ---
  if (led1Active) {
    if (currentStep < LED_COUNT && now - lastStepTime >= STEP_MS) {
      strip.setPixelColor(currentStep, strip.Color(0, 125, 125));
      strip.show();
      currentStep++;
      lastStepTime = now;
    }
    if (now - startTime >= DURATION_MS) stopAll();
  }

  if (led2Active) {
    if (currentStep < LED_COUNT && now - lastStepTime >= STEP_MS) {
      strip2.setPixelColor(currentStep, strip2.Color(255, 255, 255));
      strip2.show();
      currentStep++;
      lastStepTime = now;
    }
    if (now - startTime >= DURATION_MS) stopAll();
  }

  if (atomActive) {
    if (now - startTime >= DURATION_MS) stopAll();
  }
}