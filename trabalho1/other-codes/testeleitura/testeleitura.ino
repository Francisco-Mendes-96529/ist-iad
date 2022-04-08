int intvolt;
double doublevolt;

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
}

void loop() {
  intvolt=analogRead(A0);
  doublevolt=(double)intvolt*5/1023;
  Serial.println(doublevolt);
}
