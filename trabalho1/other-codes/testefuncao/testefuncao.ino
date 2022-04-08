int intvolt;
double doublevolt;
int funcao;

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
}

void loop() {
  /*intvolt=analogRead(A0);
  doublevolt=(double)intvolt*5/1023;
  Serial.print(intvolt);
  Serial.print(" = ");
  Serial.println(doublevolt);
  delay(1000);*/

  if(Serial.available()>0){
    funcao=(Serial.read());
    if (funcao=='3')
    {
      Serial.println("success");
    }
  }
}
