const int pinDO = 2;
const int pinAO = A0; 

void setup() {
  Serial.begin(9600);
  pinMode(pinDO, INPUT);
  
  Serial.println("Initialisation du capteur...");
}

void loop() {
  int intensite = analogRead(pinAO);
  
  int etatDigital = digitalRead(pinDO);
  
  if (etatDigital == LOW) { 
    Serial.print("AIMANT PROCHE : ");
    Serial.print("Intensite: ");
    Serial.println(intensite); 
  } else {
    // Serial.println(" [ Aucun aimant ]");
  }

  delay(150); 
}