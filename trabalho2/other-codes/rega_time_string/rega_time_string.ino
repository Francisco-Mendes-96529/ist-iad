int dia, hora, mins, seg;
void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);

}

void loop() {
  if(Serial.available()>0){
    String data = Serial.readStringUntil('\n');
    const char *stringg = data.c_str();
    Serial.println(data);
    int t = sscanf(stringg, "%d, %d:%d:%d", &dia, &hora, &mins, &seg);
    //Serial.println(t);
    switch (dia){
      case 0:
        Serial.println("Domingo");
        break;
      case 1:
        Serial.println("Segunda");
        break;
      case 2:
        Serial.println("Terça");
        break;
      case 3:
        Serial.println("Quarta");
        break;
      case 4:
        Serial.println("Quinta");
        break;
      case 5:
        Serial.println("Sexta");
        break;
      case 6:
        Serial.println("Sabado");
        break;
      default:
        Serial.println("LEITURA INVALIDA");
        break;      
    }
    Serial.flush();
  }
}
