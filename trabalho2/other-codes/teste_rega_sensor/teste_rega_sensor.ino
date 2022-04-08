int inByte = '2';
int intvolt;
double doublevolt;


void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);

}

void loop() {
  if(Serial.available()>0){
    inByte=(Serial.read());
    if(inByte=='0'){
       intvolt=analogRead(A0);
       Serial.println(intvolt);  
    }
    else {
      Serial.println("COMANDO INVALIDO");
    }
    
  }
}
