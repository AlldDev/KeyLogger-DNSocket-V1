void setup() {
  pinMode(1, OUTPUT);  // Define o pino 1 como saída
}

void loop() {
  digitalWrite(1, HIGH);  // Liga o LED
  delay(500);            // Espera 1 segundo
  digitalWrite(1, LOW);   // Desliga o LED
  delay(500);            // Espera 1 segundo
