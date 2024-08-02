#include <DigiKeyboard.h>

void setup() {
  // Inicializa o teclado
  DigiKeyboard.sendKeyStroke(0);
  // Inicia o Led
  pinMode(1, OUTPUT);
  
  // Espera um pouco para garantir que o sistema está pronto
  delay(3000);
  digitalWrite(1, HIGH);
  
  // Abre o CMD
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT); // Pressiona Win+R
  delay(1000);
  DigiKeyboard.print("cmd"); // Digita 'cmd'
  DigiKeyboard.sendKeyStroke(KEY_ENTER); // Pressiona Enter
  delay(2000);
  
  // Digita o comando 'echo Hello World' no CMD
  DigiKeyboard.print("echo Hello World");
  DigiKeyboard.sendKeyStroke(KEY_ENTER); // Pressiona Enter
  digitalWrite(1, LOW);
}

void loop() {
  // Não é necessário fazer nada no loop
}
