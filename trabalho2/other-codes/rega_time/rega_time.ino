int inByte = 'a';

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);

}

void loop() {
  if(Serial.available()>0){
    inByte=(Serial.read());
    switch (inByte){
      case '0':
        Serial.println("Domingo");
        break;
      case '1':
        Serial.println("Segunda");
        break;
      case '2':
        Serial.println("Terça");
        break;
      case '3':
        Serial.println("Quarta");
        break;
      case '4':
        Serial.println("Quinta");
        break;
      case '5':
        Serial.println("Sexta");
        break;
      case '6':
        Serial.println("Sabado");
        break;
      default:
        Serial.println("LEITURA INVALIDA");
        break;      
    }
    Serial.flush();
  }
}
