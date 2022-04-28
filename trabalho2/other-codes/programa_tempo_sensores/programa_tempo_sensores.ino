struct Programa{
  int ativo=0; //0-false, 1-true
  int d[7]={0,0,0,0,0,0,0}; //dia 0-false 1-true
  int hi=0, mi=0; //hora, minutos iniciais
  int hf=0, mf=0; //hora, minutos finais
  int canais[12]={0,0,0,0,0,0,0,0,0,0,0,0}; // 0-false 1-true
  int fonte=0; //torneira-0, bomba-1
  int sensor[2]={0,0}; // 0-false 1-true
} prog[20];

int dia, hora, mins, seg;
unsigned long start_time=0, curr_time=0, ant_time=0;
int seg_atual, min_atual, hora_atual, dia_atual;
int canal_pin[12][2]={ {2,-1},{3,-1},{4,-1},{5,-1},{6,-1},{7,-1},{8,-1},{9,-1},{10,-1},{11,-1},{12,-1},{13,-1} };
int sensor_pin[2]={A0, A1};
int nivel_humidade[2]={0,0}; //variável que guarda a voltagem lida pelo sensor
bool al3 = 1;
bool al5 = !al3;


void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready");
  for(int i = 0; i<12; i++){
    pinMode(canal_pin[i][0], OUTPUT);  
  }
  pinMode(A0, INPUT);  //sensor 1
  pinMode(A1, INPUT);  //sensor 2
  pinMode(A2, OUTPUT);  //torneira
  pinMode(A3, OUTPUT);  //bomba
  
  
}

void loop() {
  if(Serial.available()>0){
   int inByte = Serial.read();
   if (inByte=='t') tempo(); 
   if (inByte=='T') enviar_tempo(); //debug
   if (inByte=='e') enviar();
   if (inByte=='r') receber();
   if (inByte=='k') enviar_k(); //debug
   if (inByte=='a') receber_ativo(); 
   if (inByte=='s') leitura_sensores(); //debug
  }
  tempo_atual();
  for (int i=0; i<20; i++){
    if (prog[i].ativo){
      int mi=prog[i].mi;
      int mf=prog[i].mf;
      int hi= prog[i].hi;
      int hf =prog[i].hf;
      if(prog[i].d[dia_atual]==1 && ((hi==hf && hora_atual==hi && min_atual>=mi && min_atual<mf) || (hi!=hf && ((hora_atual>hi && hora_atual<hf) || (hora_atual==hi && min_atual>=mi) || (hora_atual==hf && min_atual<mf)))))
      {
        if(prog[i].sensor[0]==1 || prog[i].sensor[1]==1){
          nivel_humidade[0] = analogRead(sensor_pin[0])*prog[i].sensor[0]; //se estiver desligado, entao dá 0, nao contribui para a decisao de regar
          nivel_humidade[1] = analogRead(sensor_pin[1])*prog[i].sensor[1];
          if(nivel_humidade[0] > 285*al3 + 629*al5 || nivel_humidade[1] > 285*al3 + 629*al5){
            regar(i);
          }
            else{
              //parar de regar se ambos estiverem muito humidos
              parar_regar(i);
            }
        }
        else{
          //se ambos os sensores estiverem desligados, rega
          regar(i);
        }
      }
      else{
        //se nao estiver na hora de rega, para de regar
        parar_regar(i);
      }
    }
    else{
      //se nao estiver ativo
      parar_regar(i);
    }
  }
}

void regar(int i){ 
  digitalWrite(A2, !prog[i].fonte);
   digitalWrite(A3, prog[i].fonte);
   for(int j = 0; j<12; j++){
      if(prog[i].canais[j]==1) {
        canal_pin[j][1]=i;
        digitalWrite(canal_pin[j][0], 1);
      }
   }
}

void parar_regar(int i){
  for(int k = 0; k<12; k++){
    if(canal_pin[k][1]==i){
      canal_pin[k][1]=-1;
      digitalWrite(canal_pin[k][0], 0);
    }
  }
}

void leitura_sensores(){
  for(int k=0; k<2; k++){
    nivel_humidade[k] = analogRead(sensor_pin[k]);
    if(nivel_humidade[k] >= 377*al3 + 749*al5 && nivel_humidade[k] <= 437*al3 + 807*al5){
      String temp= "Ar: " + String(nivel_humidade[k]);
      Serial.println(temp);
      }
    else if(nivel_humidade[k] > 327*al3 + 726*al5 && nivel_humidade[k] <= 377*al3 + 749*al5){
      String temp= "Solo seco: " + String(nivel_humidade[k]);
      Serial.println(temp);
    }
    else if(nivel_humidade[k] > 285*al3 + 629*al5 && nivel_humidade[k] <= 327*al3 + 726*al5){
      String temp= "Solo meio húmido: " + String(nivel_humidade[k]);
      Serial.println(temp);
    }
    else if(nivel_humidade[k] > 258*al3 + 535*al5 && nivel_humidade[k] <= 285*al3 + 629*al5){
      String temp= "Solo húmido: " + String(nivel_humidade[k]);
      Serial.println(temp);
    }
    else if(nivel_humidade[k] > 223*al3 + 473*al5 && nivel_humidade[k] <= 258*al3 + 535*al5){
      String temp= "Água: " + String(nivel_humidade[k]);
      Serial.println(temp);
    }
    else{
      Serial.println("Valor lido inválido. Verifique a qualidade do sensor ou da ligação :):");
    }
  }
}

void tempo() {
  while (true) {
    if(Serial.available()>0){
      String data = Serial.readStringUntil('\n');
      int t = sscanf(data.c_str(), "%d, %d:%d:%d", &dia, &hora, &mins, &seg);
      if (t==4){
        Serial.println("LEITURA VALIDA");
        seg_atual=seg;
        min_atual=mins;
        hora_atual=hora;
        dia_atual=dia;
        start_time=millis()/1000;
        ant_time = start_time;
        break;
      }
      else Serial.println("LEITURA INVALIDA");
      Serial.flush();
    }
  }
}

void tempo_atual(){
  curr_time=millis()/1000;
  unsigned long diff_times=curr_time-ant_time;
  seg_atual += diff_times;
  while (seg_atual>=60){
    seg_atual -= 60;
    min_atual += 1;
  }
  while(min_atual>=60){
    min_atual -= 60;
    hora_atual += 1;
  }
  while(hora_atual>=24){
    hora_atual -= 24;
    dia_atual += 1;
  }
  while(dia_atual>=7) dia_atual -= 7;
  ant_time = curr_time;
}

void enviar_tempo() // função de debug do tempo enviado pelo Raspberry PI inicialmente e do tempo atual
{
  String strtempo =  " -- Dia: " + String(dia) + " -- " + String(hora) + ":" + String(mins) + ":" + String(seg) + " -- Dia: " + String(dia_atual) + " -- " + String(hora_atual) + ":" + String(min_atual) + ":" + String(seg_atual);
  Serial.println(strtempo);
  Serial.flush();
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
