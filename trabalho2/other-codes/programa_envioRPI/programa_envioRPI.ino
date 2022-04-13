struct Programa{
  int d[7]={0,0,0,0,0,0,0}; //dia
  int h=0, m=0; //hora, minutos
  int canais[12]={0,0,0,0,0,0,0,0,0,0,0,0};
  int fonte=0; //torneira-0, bomba-1
  int sensor=0; //0, 1, 2 sensores ligados
}prog[20];

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready");
}

void loop() {
  if(Serial.available()>0){
   int inByte = Serial.read();
   if (inByte=='e') enviar();
  }
}

void enviar(){
  for (int i=0; i<20; i++)
  {
    for (int j=0; j<7; j++)
    {
      Serial.println(prog[i].d[j]);
      Serial.flush();
    }
    Serial.println(prog[i].h);
    Serial.flush();
    Serial.println(prog[i].m);
    Serial.flush();
    for (int j=0; j<12; j++)
    {
      Serial.println(prog[i].canais[j]);
      Serial.flush();
    }
    Serial.println(prog[i].fonte);
    Serial.flush();
    Serial.println(prog[i].sensor);
    Serial.flush();
  }
}
