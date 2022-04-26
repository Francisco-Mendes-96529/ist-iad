struct Programa{
  int ativo=0; //0-false, 1-true
  int d[7]={0,0,0,0,0,0,0}; //dia 0-false 2-true
  int hi=0, mi=0; //hora, minutos iniciais
  int hf=0, mf=0; //hora, minutos finais
  int canais[12]={0,0,0,0,0,0,0,0,0,0,0,0}; // 0-false 2-true
  int fonte=0; //torneira-0, bomba-1
  int sensor[2]={0,0}; // 0-false 2-true
}prog[20];

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready");
  prog[0].ativo=1;
  prog[0].hi=12;
  prog[0].mi=30;
  prog[4].ativo=1;
  prog[4].d[1]=2;
  prog[4].d[2]=2;
  prog[4].hi=12;
  prog[4].mi=30;
  prog[4].canais[1]=2; 
  prog[4].hf=12;
  prog[4].mf=45;
  prog[4].fonte=1;
  prog[4].sensor[0]=2;
}

void loop() {
  if(Serial.available()>0){
   int inByte = Serial.read();
   if (inByte=='e') enviar();
   if (inByte=='r') receber();
   if (inByte=='k') enviar_k();
   if (inByte=='a') receber_ativo();
  }
}

void receber(){
  Serial.println("recebendo...");
  Serial.flush();
  int k = Serial.readStringUntil('\n').toInt();


  prog[k].ativo = Serial.readStringUntil('\n').toInt();
  for (int j=0; j<7; j++)
    {
      prog[k].d[j]=Serial.readStringUntil('\n').toInt();
    }
  prog[k].hi = Serial.readStringUntil('\n').toInt();
  prog[k].mi = Serial.readStringUntil('\n').toInt();
  prog[k].hf = Serial.readStringUntil('\n').toInt();
  prog[k].mf = Serial.readStringUntil('\n').toInt();
  for (int j=0; j<12; j++)
    {
      prog[k].canais[j]= Serial.readStringUntil('\n').toInt();
    }  
  prog[k].fonte = Serial.readStringUntil('\n').toInt();
  for (int j=0; j<2; j++)
    {
      prog[k].sensor[j]= Serial.readStringUntil('\n').toInt();
    }
    //Serial.println("acabou de receber");
}

void receber_ativo(){
  Serial.println("recebendo ativo...");
  Serial.flush();
  int k = Serial.readStringUntil('\n').toInt();
  prog[k].ativo = Serial.readStringUntil('\n').toInt();
}

void enviar(){
  for (int i=0; i<20; i++)
  {
    Serial.println(prog[i].ativo);
    Serial.flush();
    for (int j=0; j<7; j++)
    {
      Serial.println(prog[i].d[j]);
      Serial.flush();
    }
    Serial.println(prog[i].hi);
    Serial.flush();
    Serial.println(prog[i].mi);
    Serial.flush();
    Serial.println(prog[i].hf);
    Serial.flush();
    Serial.println(prog[i].mf);
    Serial.flush();
    for (int j=0; j<12; j++)
    {
      Serial.println(prog[i].canais[j]);
      Serial.flush();
    }
    Serial.println(prog[i].fonte);
    Serial.flush();
    Serial.println(prog[i].sensor[0]);
    Serial.flush();
    Serial.println(prog[i].sensor[1]);
    Serial.flush();
  }  
}

void enviar_k(){  
  int k = Serial.readStringUntil('\n').toInt();
  Serial.println(k);
    Serial.println(prog[k].ativo);
    Serial.flush();
    for (int j=0; j<7; j++)
    {
      Serial.println(prog[k].d[j]);
      Serial.flush();
    }
    Serial.println(prog[k].hi);
    Serial.flush();
    Serial.println(prog[k].mi);
    Serial.flush();
    Serial.println(prog[k].hf);
    Serial.flush();
    Serial.println(prog[k].mf);
    Serial.flush();
    for (int j=0; j<12; j++)
    {
      Serial.println(prog[k].canais[j]);
      Serial.flush();
    }
    Serial.println(prog[k].fonte);
    Serial.flush();
    Serial.println(prog[k].sensor[0]);
    Serial.flush();
    Serial.println(prog[k].sensor[1]);
    Serial.flush(); 
}
