int dia, hora, mins, seg;
int start_time;

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready");
  pinMode(A0, INPUT);

}

void loop() {
  if(Serial.available()>0){
   int inByte = Serial.read();
   if (inByte=='t') tempo();
  }
}

void tempo() {
  while (true) {
    if(Serial.available()>0){
      String data = Serial.readStringUntil('\n');
      //Serial.println(data);
      int t = sscanf(data.c_str(), "%d, %d:%d:%d", &dia, &hora, &mins, &seg);
      //Serial.println(t);
      if (t==4){
        Serial.println("LEITURA VALIDA");
        start_time=millis();
        break;
      }
      else Serial.println("LEITURA INVALIDA");
      Serial.flush();
    }
  }
}
