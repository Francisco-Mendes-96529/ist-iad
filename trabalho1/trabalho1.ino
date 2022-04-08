int inByte = '1'; // Variável de leitura do comando enviado pelo Raspberry PI
int intvolt; // Variável que guarda o valor no pin A0
double doublevolt; // Valor real do intvolt

void setup() {    
  Serial.begin(9600); 
  pinMode(A0, INPUT); // Inicializar pin A0 como input

}

void loop() {
  if(Serial.available()>0){ // Testar se há algo escrito no buffer enviado pelo Raspberry PI
    inByte=(Serial.read()); // Leitura do que está no buffer
    // Testar se o comando enviado pelo Raspberry PI é válido
    if(inByte=='0'){ 
       intvolt=analogRead(A0); // Leitura do valor no pin A0 (range inteiro [0,1023])
       doublevolt=(double)intvolt*5/1023; // Normalização do valor do pin A0 no range double [0,5]
       Serial.println(doublevolt);  // Escrever no buffer o valor lido 
    }
    else {
      Serial.println("COMANDO INVALIDO"); 
    }
    
  }
}
