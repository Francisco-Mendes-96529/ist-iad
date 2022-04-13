int dia, hora, mins, seg;
void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready");
  pinMode(A0, INPUT);

}

void loop() {
  if(Serial.available()>0){
    String data = Serial.readStringUntil('\n');
    //Serial.println(data);
    int t = sscanf(data.c_str(), "%d, %d:%d:%d", &dia, &hora, &mins, &seg);
    //Serial.println(t);
    if (t==4){
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
    }
    else Serial.println("LEITURA INVALIDA");
    Serial.flush();
  }
}
