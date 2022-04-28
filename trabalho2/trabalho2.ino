struct Programa{
  int ativo=0; //0-false, 1-true
  int d[7]={0,0,0,0,0,0,0}; //dia 0-false 1-true
  int hi=0, mi=0; // hora, minutos iniciais
  int hf=0, mf=0; // hora, minutos finais
  int canais[12]={0,0,0,0,0,0,0,0,0,0,0,0}; // 0-false 1-true
  int fonte=0; //torneira-0, bomba-1
  int sensor[2]={0,0}; // 0-false 1-true
} prog[20];

int dia, hora, mins, seg; // variáveis  que guardam o instante inicial
unsigned long start_time=0, curr_time=0, ant_time=0; // instante inicial em milisegundos do Arduino; instante atual em milisegundos do Arduino; instante anterior em ms
int seg_atual, min_atual, hora_atual, dia_atual; // variáveis que guardam a hora lida pelo Arduino quando for ligado ao RaspberryPi
int canal_pin[12][2]={ {2,-1},{3,-1},{4,-1},{5,-1},{6,-1},{7,-1},{8,-1},{9,-1},{10,-1},{11,-1},{12,-1},{13,-1} }; // Matriz que associa ao número de cada pin o programa que o ligou (default = -1)
int sensor_pin[2]={A0, A1}; //Array que guarda os pins analógicos que correspondem aos sensores
int nivel_humidade[2]={0,0}; //variável que guarda a voltagem lida pelo sensor
bool al3 = 1; //variável boleana auxiliar que indica que a tensão ligada ao sensor é 3.3 Volts
bool al5 = !al3; //variável boleana auxiliar que indica que a tensão ligada ao sensor é 5 Volts (complementar à variàvel anterior)


void setup() {
  Serial.begin(9600); // Definir  a taxa de dados em bits por segundo para transmissão serial de dados com o valor 9600
  Serial.println("Arduino is ready"); //Assinalar a prontidão do Arduino
  for(int i = 0; i<12; i++){
    pinMode(canal_pin[i][0], OUTPUT); //Definir os pins digitais como outputs 
  }
  pinMode(A0, INPUT);  //Definir o A0 como sensor 1
  pinMode(A1, INPUT);  //Definir o A1 como sensor 2
  pinMode(A2, OUTPUT);  //Definir o A2 como torneira
  pinMode(A3, OUTPUT);  //Definir o A3 como bomba
}

void loop() {
  if(Serial.available()>0){
   int inByte = Serial.read();
   if (inByte=='t') tempo(); // Ler tempo
   if (inByte=='T') enviar_tempo(); //debug
   if (inByte=='r') receber(); // Receber configurações programa
   if (inByte=='k') enviar_k(); //debug
   if (inByte=='a') receber_ativo();  // Receber ativo
   if (inByte=='s') leitura_sensores();  // Ler os valores dos sensores
  }
  
  tempo_atual(); //atualizar o tempo
  
  for (int i=0; i<20; i++){
    if (prog[i].ativo){
      char hi[4], hf[4], ha[4]; // Juntar os dígitos das horas e minutos numa string
      sprintf (hi, "%02d%02d", prog[i].hi,prog[i].mi); // escrita de prog[i].hi e prog[i].mi em hi
      sprintf (hf, "%02d%02d", prog[i].hf,prog[i].mf); // escrita de prog[i].hf e prog[i].mf em hf
      sprintf (ha, "%02d%02d", hora_atual, min_atual);  // escrita dehora_atual e min_atual em ha
      if(prog[i].d[dia_atual]==1 && strcmp(ha,hi)>=0 && (strcmp(hf,ha)>0 || strcmp(hf, "0000")==0) )
      {
        if(prog[i].sensor[0]==1 || prog[i].sensor[1]==1){ //Escrita de valores dos sensores caso pelo menos um esteja ligado
          nivel_humidade[0] = analogRead(sensor_pin[0])*prog[i].sensor[0]; //se o sensor estiver desligado, entao dá 0, nao contribui para a decisao de regar
          nivel_humidade[1] = analogRead(sensor_pin[1])*prog[i].sensor[1]; //se o sensor estiver desligado, entao dá 0, nao contribui para a decisao de regar
          if(nivel_humidade[0] > 285*al3 + 629*al5 || nivel_humidade[1] > 285*al3 + 629*al5){
            regar(i); // Regar caso o nível de humidade seja superior ao nível de humidade do solo semi húmido
          }
            else{
              //parar de regar se ambos os sensores estiverem muito humidos
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

void regar(int i){ //liga os pinos associados aos canais de rega do programa i e ativa a fonte escolhida
   digitalWrite(A2, !prog[i].fonte);
   digitalWrite(A3, prog[i].fonte);
   for(int j = 0; j<12; j++){
      if(prog[i].canais[j]==1) { // se o canal do programa estiver ligado, liga o pino do canal correspondente 
        canal_pin[j][1]=i; // associa ao pin o programa que o ligou
        digitalWrite(canal_pin[j][0], 1);
      }
   }
}

void parar_regar(int i){ //desliga os pinos associados aos canais de rega do programa i
  for(int k = 0; k<12; k++){
    if(canal_pin[k][1]==i){
      canal_pin[k][1]=-1;// desassocia do pin o programa que o ligou, colocando o valor de default
      digitalWrite(canal_pin[k][0], 0);
    }
  }
}

void leitura_sensores(){ //faz a leitura dos sensores de humidade e diz o valor e a categoria (ar, solo seco, ...)
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
      Serial.println("Valor lido inválido. Verifique a qualidade do sensor ou da ligação");
    }
  }
}

void tempo(){ // função que recebe o tempo inicial do Raspberry Pi
  while (true) {
  if(Serial.available()>0){
    String data = Serial.readStringUntil('\n');
    int t = sscanf(data.c_str(), "%d, %d:%d:%d", &dia, &hora, &mins, &seg); //guarda nas variaveis dia, hora, mins, seg os instantes iniciais recebidos
    if (t==4){ //se todas as leituras e atribuições de variaveis forem válidas
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

void tempo_atual(){ //função que atualiza o tempo 
  curr_time=millis()/1000; //segundos desde que o Arduino ligou
  unsigned long diff_time=curr_time-ant_time; 
  if(diff_time<0) diff_time = ULONG_MAX/1000 - ant_time + curr_time;
  seg_atual += diff_time;
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

void enviar_tempo() { // função de debug do tempo enviado pelo Raspberry PI inicialmente e do tempo atual
  String strtempo =  " -- Dia: " + String(dia) + " -- " + String(hora) + ":" + String(mins) + ":" + String(seg) + " -- Dia: " + String(dia_atual) + " -- " + String(hora_atual) + ":" + String(min_atual) + ":" + String(seg_atual);
  Serial.println(strtempo);
  Serial.flush();
}

void receber() // função que recebe do Raspberry PI as especificações do programa k
{
  Serial.println("recebendo...");
  Serial.flush();
  int k = Serial.readStringUntil('\n').toInt(); //indice do programa
  //ler todas as especificações do Raspberry PI
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
}

void receber_ativo() //função que recebe a ordem do Raspberry PI para ativar/desativar o programa k (sem mudar outras especificações do programa)
{
  Serial.println("recebendo ativo...");
  Serial.flush();
  int k = Serial.readStringUntil('\n').toInt(); //programa a ativar/desativar
  prog[k].ativo = Serial.readStringUntil('\n').toInt();
}

void enviar_k() //função de debug que envia ao Raspberry PI as especificações do programa k
{  
  int k = Serial.readStringUntil('\n').toInt(); //índice do programa que está a ser pedido pelo Raspberry PI
  Serial.println(k);
  //impressão das especificações
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
