const int pinBouton = 3; // Le bouton est sur la pin D3

void setup() {
  Serial.begin(9600);
  pinMode(pinBouton, INPUT_PULLUP); 
  Serial.println("Prêt à détecter l'appui...");
}

void loop() {
  int etatBouton = digitalRead(pinBouton);

  if (etatBouton == LOW) {
    Serial.println("Bouton APPUYÉ !");
    delay(200);
  }
}