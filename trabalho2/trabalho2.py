import numpy as np
import serial
import PyQt5
import pyqtgraph as pg
import sys  
import os
from PyQt5 import QtWidgets, QtCore
import time

#DEBUG
DEBUG = False

# Definir porta para ligação ao Arduino (se não encontrar termina o programa)
if os.path.exists('/dev/ttyACM0'):
    dev_name = '/dev/ttyACM0'
elif os.path.exists('/dev/ttyACM1'):
    dev_name = '/dev/ttyACM1'
elif os.path.exists('/dev/ttyACM2'):
    dev_name = '/dev/ttyACM2'
else:
    print("Não foi encontrado o Arduino")
    sys.exit()

#variaveis globais
lastProg = 0 #variavel que guarda o indice do programa anterior quando se tenta mudar o programa

my_file = 'progs_rega.txt' #ficheiro de texto que guarda a informação dos programas

# Lista de 20 dicionários (programas)
Prog = [{'A':0, 'D':[0,0,0,0,0,0,0], "Hi":0, "Mi":0, "Hf":0, "Mf":0, "Canal":[0,0,0,0,0,0,0,0,0,0,0,0], "Fonte":0, "Sensor":[0,0]} for i in range(20)]

# Funções de comunicação com o Arduino
def serialWrite(var): #Função que transforma um inteiro numa string (com um \n) e escreve no Arduino
    ser.write((str(var)+"\n").encode('utf-8'))

def initArduino(): # Função que aguarda até ao Arduino estar pronto
    while True:
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        if line=="Arduino is ready":
            if DEBUG: print(line)
            break
        
def read_file(): #Função que lê o ficheiro que guarda os programas e atribui os valores do ficheiro às variáveis 
    if os.path.isfile(my_file): #Testar se o ficheiro existe 
        f = open(my_file, "r")
        data = f.readlines()
        for i in range(20):
            Prog[i]['A'] = int(data[1+i*9].split()[1])
            temp = data[2+i*9].split()
            for j in range(7):
                Prog[i]['D'][j] = int(temp[j+1])
            temp = data[3+i*9].split()
            Prog[i]['Hi'] = int(temp[1])
            Prog[i]['Mi'] = int(temp[2])
            temp = data[4+i*9].split()
            Prog[i]['Hf'] = int(temp[1])
            Prog[i]['Mf'] = int(temp[2])
            temp = data[5+i*9].split()
            for j in range(12):
                Prog[i]['Canal'][j] = int(temp[j+1])
            Prog[i]['Fonte'] = int(data[6+i*9].split()[1])
            temp = data[7+i*9].split()
            Prog[i]['Sensor'][0] = int(temp[1])
            Prog[i]['Sensor'][1] = int(temp[2])
        f.close()
        if DEBUG: print("leitura sucedida")
    else:
        save_file() # Se não existir vai criar um ficheiro com todas as variáveis a zero

def save_file(): # Função que guarda no ficheiro as variáveis (se não existir cria um com as variáveis todas a 0)
    f = open(my_file,"wt") 
    for i in range(20):
        f.write("Prog: "+str(i+1)+"\n")
        f.write("Ativo: "+str(Prog[i]['A'])+"\n")
        f.write("Dias:")
        for j in range(7):
            f.write(" "+str(Prog[i]['D'][j]))
        f.write("\n")
        f.write("Hi: "+str(Prog[i]['Hi'])+" "+str(Prog[i]['Mi'])+"\n")
        f.write("Hf: "+str(Prog[i]['Hf'])+" "+str(Prog[i]['Mf'])+"\n")
        f.write("Canais:")
        for j in range(12):
            f.write(" "+str(Prog[i]['Canal'][j]))
        f.write("\n")
        f.write("Fonte: "+str(Prog[i]['Fonte'])+"\n")
        f.write("Sensores: "+str(Prog[i]['Sensor'][0])+" "+str(Prog[i]['Sensor'][1])+"\n")
        f.write("\n")
    f.close()

def enviar(k): # Função que envia a as especificações do programa k para o Arduino
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('r'.encode('utf-8')) # A escrita deste byte ativa a receção no Arduino
    if DEBUG: print(ser.readline().decode('utf-8').rstrip())
    serialWrite(k) #Enviar o índice do programa 
    serialWrite(Prog[k]['A'])
    for j in range(7):
        serialWrite(Prog[k]['D'][j])
    serialWrite(Prog[k]['Hi'])
    serialWrite(Prog[k]['Mi'])
    serialWrite(Prog[k]['Hf'])
    serialWrite(Prog[k]['Mf'])
    for j in range(12):
        serialWrite(Prog[k]['Canal'][j])
    serialWrite(Prog[k]['Fonte'])
    serialWrite(Prog[k]['Sensor'][0])
    serialWrite(Prog[k]['Sensor'][1])
        
def receber_k(k): # Função debug- recebe do Arduino o programa k
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('k'.encode('utf-8'))
    serialWrite(k)
    print(ser.readline().decode('utf-8').rstrip())
    for i in range(27):
        print(ser.readline().decode('utf-8').rstrip())

def initTempo(): # Função que envia o instante de tempo inicial
    today = time.strftime("%w, %H:%M:%S")
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(today.encode('utf-8'))
    while True:
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        if line=="LEITURA VALIDA": # se o Arduino consegue ler o tempo corretamente 
            if DEBUG: print("leitura do tempo sucedida")
            break
        elif line=="LEITURA INVALIDA":
            today = time.strftime("%w, %H:%M:%S")
            ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
            ser.write(today.encode('utf-8'))

def debugTempo(): #Função que recebe o tempo atual do Arduino
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('T'.encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
    print(line)

def debugSensores(): #Função que recebe a leitura dos sensores do Arduino. Recebe o nivel de humidade e a categoria (ar, solo húmido, solo seco, solo semi humido, agua)
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('s'.encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip() 
    print("Sensor 1: "+line)
    line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
    print("Sensor 2: "+line)

# Transforma os algarismos da SpinBox para terem 2 dígitos
class DoubleDigitSpinBox(QtWidgets.QSpinBox):
    def __init__(self, *args):
       QtWidgets.QSpinBox.__init__(self, *args)

    def textFromValue(self, value):
       return "%02d" % value

# classe de janelas secundárias
class subWindow(QtWidgets.QWidget): # Classe da janela secundária
    def createWindow(self,width,height):
        parent = None
        super(subWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint) # Janela secundária em cima da main e sem barra superior
        self.setMinimumSize(width,height)
        self.setMaximumSize(width,height)
        # Centrar janela no ecrã
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

# Classe da janela principal
class MainWindow(QtWidgets.QMainWindow):

    # Função que inicializa as propriedades da janela, dos botões e gráfico
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

# MainWindow
        self.setWindowTitle("Trabalho 2 - Sistema de Rega")
        # Dimensões
        self.setMinimumSize(900,500)
        self.setMaximumSize(900,500)
        # Centrar janela no ecrã
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


# Drop down list Programas: contém os vários programas
        self.progList = QtWidgets.QComboBox(self)
        self.progList.addItems([str(i+1) for i in range(20)])
        self.progList.setGeometry(490, 0, 50, 50)
        self.progList.currentIndexChanged.connect(self.progFunction) #Quando se muda o programa chama a função progFunction
        
# Labels    
        self.progLabel = QtWidgets.QLabel("Programa", self)
        self.diasLabel = QtWidgets.QLabel("Dias", self)
        self.canaisLabel = QtWidgets.QLabel("Canais", self)
        self.hiLabel = QtWidgets.QLabel("Início:", self)
        self.hfLabel = QtWidgets.QLabel("Fim:", self)
        self.fonteLabel = QtWidgets.QLabel("Fonte", self)
        self.sensoresLabel = QtWidgets.QLabel("Sensores", self)
        self.doisPontosI = QtWidgets.QLabel(":", self)
        self.doisPontosF = QtWidgets.QLabel(":", self)

# Posições Labels
        self.progLabel.setGeometry(375, 0, 100, 50)
        self.diasLabel.setGeometry(100, 50, 100, 50)
        self.canaisLabel.setGeometry(733, 50, 100, 50)
        self.hiLabel.setGeometry(330, 100, 100, 50)
        self.hfLabel.setGeometry(330, 165, 100, 50)
        self.sensoresLabel.setGeometry(400, 240, 100, 50)
        self.fonteLabel.setGeometry(415, 340, 100, 50)
        
# Checkboxes dias - Permite selecionar os dias 
        self.diaName = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.dia = [QtWidgets.QCheckBox(self.diaName[i], self)for i in range(7)]
        for i in range(7):
            self.dia[i].setGeometry(75, 50*i+100, 110, 50)
        
# Checkboxes canais Permite selecionar os canais
        self.canais = [QtWidgets.QCheckBox(str(i+1), self)for i in range(12)]
        for i in range(6):
            self.canais[i].setGeometry(710, 50*i+100, 100, 50)
            self.canais[i+6].setGeometry(790, 50*i+100, 100, 50)

# Checkboxes sensores
        self.sensor = [QtWidgets.QCheckBox(str(i+1), self)for i in range(2)]
        self.sensor[0].setGeometry(380, 280, 100, 50)
        self.sensor[1].setGeometry(480, 280, 100, 50)
        
# Selecionar Fonte - Radio button que permite selecionar ou a bomba ou a torneira como fonte
        self.fonte1 = QtWidgets.QRadioButton("Torneira", self)
        self.fonte2 = QtWidgets.QRadioButton("Bomba", self)
        self.fonte1.setGeometry(325, 380, 100, 50)
        self.fonte2.setGeometry(465, 380, 100, 50)

# Hora inicial e final
        self.horaInicial = DoubleDigitSpinBox(self)
        self.minInicial = DoubleDigitSpinBox(self)
        self.horaFinal = DoubleDigitSpinBox(self)
        self.minFinal = DoubleDigitSpinBox(self)
        self.horaInicial.setGeometry(400,100,65,50)
        self.minInicial.setGeometry(480,100,65,50)
        self.doisPontosI.setGeometry(465,100,15,50)
        self.doisPontosI.setAlignment(QtCore.Qt.AlignCenter)
        self.horaFinal.setGeometry(400,165,65,50)
        self.minFinal.setGeometry(480,165,65,50)
        self.doisPontosF.setGeometry(465,165,15,50)
        self.doisPontosF.setAlignment(QtCore.Qt.AlignCenter)
        self.horaInicial.setRange(0,23)
        self.minInicial.setRange(0,59)
        self.horaFinal.setRange(0,23)
        self.minFinal.setRange(0,59)
        self.horaInicial.setAlignment(QtCore.Qt.AlignCenter)
        self.horaFinal.setAlignment(QtCore.Qt.AlignCenter)
        self.minInicial.setAlignment(QtCore.Qt.AlignCenter)
        self.minFinal.setAlignment(QtCore.Qt.AlignCenter)

# Botões Guardar e Ativo - Guarda/edita e ativa o programa, respetivamente
        self.guardar = QtWidgets.QPushButton("Editar",self)
        self.guardar.setCheckable(True) # Permite 2 estados associados ao mesmo botão: Guardar (está no modo de editar, isChecked()=1) e Editar (está guardado, isChecked()=0)
        self.guardar.setGeometry(760,420,100,50)
        self.guardar.toggled.connect(self.guardarFunction)
        self.ativo = QtWidgets.QPushButton("OFF",self)
        self.ativo.setCheckable(True) # Permite 2 estados associados ao mesmo botão: ON (isChecked()=1) e OFF (isChecked()=0)
        self.ativo.setGeometry(680,420,70,50)
        self.ativo.toggled.connect(self.on_off)
        self.ativo.setStyleSheet("background-color : rgb(255,100,100)") # VERMELHO

# Botão que mostra os programas ativos
        self.progAtivosButton = QtWidgets.QPushButton("Info\nProgramas",self)
        self.progAtivosButton.clicked.connect(self.progAtivosFunction)
        self.progAtivosButton.setGeometry(800,0,100,60)

# Botão debug
        if DEBUG:
            self.debugButton = QtWidgets.QPushButton("Debug",self)
            self.debugButton.clicked.connect(self.debugFunction)
        
# After Functions
        self.createNotSavedWindow() #Cria a janela de aviso quando há alterações não guardadas
        self.createWarningWindow() #Cria a janela de aviso quando há conflitos dentro de um programa ou entre programas
        #self.createInfoWindow() #Cria a janela de informação de programas
        self.varCloseEvent = 0 # = 1 quando estamos a editar e tentamos fechar a mainWindow
        self.progFunction()
        self.infoWindow = None
        
# Funções
    def closeEvent(self, event):
        if self.notSavedWindow.isVisible() or self.warningWindow.isVisible() or (0 if not self.infoWindow else self.infoWindow.isVisible()): # Se uma janela secundária estiver visivel, ignora a tentativa de encerro da main window
            event.ignore()
        elif self.guardar.isChecked(): #Há alterações por guardar
            self.varCloseEvent = 1
            self.setEnabled(0) #desativar a main window
            self.notSavedWindow.show() #mostrar a janela de alterações não guardadas
            event.ignore() #ignora a tentativa de encerro da main window
        else:
            save_file() # guardar no ficheiro 
            event.accept() # encerrar a main window
        
    def progFunction(self):
        global lastProg
        k = self.progList.currentIndex() # variável que contém o indice do programa para o qual o utilizador pretende mudar para
        if self.guardar.isChecked(): # se tentar mudar de programa com alterações não guardadas
            if not self.warningWindow.isVisible(): # caso se tente guardar quando existem conflitos
                self.setEnabled(0)
                self.notSavedWindow.show()
        else: # se tentar mudar de programa já guardado 
            lastProg = k
            # trazer as especificações do novo programa - aquele para que mudamos
            self.ativo.setChecked(Prog[k]['A'])
            for i in range(7):
                self.dia[i].setChecked(Prog[k]['D'][i])
            self.horaInicial.setValue(Prog[k]['Hi'])
            self.minInicial.setValue(Prog[k]['Mi'])
            self.horaFinal.setValue(Prog[k]['Hf'])
            self.minFinal.setValue(Prog[k]['Mf'])
            for i in range(12):
                self.canais[i].setChecked(Prog[k]['Canal'][i])
            self.fonte1.setChecked(not Prog[k]['Fonte'])
            self.fonte2.setChecked(Prog[k]['Fonte'])
            self.sensor[0].setChecked(Prog[k]['Sensor'][0])
            self.sensor[1].setChecked(Prog[k]['Sensor'][1])
            
            # disable buttons
            for i in range(7):
                self.dia[i].setEnabled(0)
            self.horaInicial.setEnabled(0)
            self.minInicial.setEnabled(0)
            self.horaFinal.setEnabled(0)
            self.minFinal.setEnabled(0)
            for i in range(12):
                self.canais[i].setEnabled(0)
            self.fonte1.setEnabled(0)
            self.fonte2.setEnabled(0)
            self.sensor[0].setEnabled(0)
            self.sensor[1].setEnabled(0)
            
    def guardarFunction(self): #função chamada quando o botão de guardar/editar muda de estado
        if self.guardar.isChecked(): # entrar no modo de edição - ativar todos os botões
            self.guardar.setText("Guardar")
            for i in range(7):
                self.dia[i].setEnabled(1)
            self.horaInicial.setEnabled(1)
            self.minInicial.setEnabled(1)
            self.horaFinal.setEnabled(1)
            self.minFinal.setEnabled(1)
            for i in range(12):
                self.canais[i].setEnabled(1)
            self.fonte1.setEnabled(1)
            self.fonte2.setEnabled(1)
            self.sensor[0].setEnabled(1)
            self.sensor[1].setEnabled(1)
        else: # guardar - queremos desativar todos os botões até o utilizador entrar no modo de edição
            self.guardar.setText("Editar")
            for i in range(7):
                self.dia[i].setEnabled(0)
            self.horaInicial.setEnabled(0)
            self.minInicial.setEnabled(0)
            self.horaFinal.setEnabled(0)
            self.minFinal.setEnabled(0)
            for i in range(12):
                self.canais[i].setEnabled(0)
            self.fonte1.setEnabled(0)
            self.fonte2.setEnabled(0)
            self.sensor[0].setEnabled(0)
            self.sensor[1].setEnabled(0)
            
            k = self.progList.currentIndex()
            if  k == lastProg and not self.varCloseEvent: # evitar que quando se fecha a main window guarde os programas indevidamente
                self.guardarProg(k)
                
    def guardarProg(self,index):
        #se não houver conflito (comparação entre programas)
        if self.comparar():
            #guardar as especificações editadas
            for i in range(7):
                Prog[index]['D'][i] = int(self.dia[i].isChecked())
            Prog[index]['Hi'] = self.horaInicial.value()
            Prog[index]['Mi'] = self.minInicial.value()
            Prog[index]['Hf'] = self.horaFinal.value()
            Prog[index]['Mf'] = self.minFinal.value()
            for i in range(12):
                Prog[index]['Canal'][i] = int(self.canais[i].isChecked())
            Prog[index]['Fonte'] = int(self.fonte2.isChecked())
            Prog[index]['Sensor'][0] = int(self.sensor[0].isChecked())
            Prog[index]['Sensor'][1] = int(self.sensor[1].isChecked())
            enviar(index)
        else:
            self.guardar.setChecked(1)
        
    
    def comparar(self) -> bool: # Função que testa o programa que se está a tentar ativar para conflitos dentro do programa ou entre programas
        hInicio = "%02d%02d" % (self.horaInicial.value(), self.minInicial.value()) #converter a hora inicial no formato "hhmm"
        hFim = "%02d%02d" % (self.horaFinal.value(), self.minFinal.value()) #converter a hora final no formato "hhmm"
        if DEBUG: print(hFim == '0000')
        if hFim > hInicio or hFim == "0000": #testar se a hora final é depois da hora inicial (exceção minuto)
            dia_test = 0
            canal_test = 0
            for i in range(7):
                dia_test = self.dia[i].isChecked() # testar se algum dia está ativo
                if dia_test: break
            for i in range(12):
                canal_test = self.canais[i].isChecked() #teste se algum canal está ativo 
                if canal_test: break
            if dia_test and canal_test: #se houverem dias e canais ativos
                if self.ativo.isChecked(): 
                    canal_list = []
                    fonte_list = []
                    for i in range(20):
                        if Prog[i]['A'] and not i == lastProg: # testar os restantes programas ativos para conflitos com o programa atual
                            dia_test = 0
                            if DEBUG: print(dia_test)
                            for j in range(7):
                                if self.dia[j].isChecked() and Prog[i]['D'][j]: #testar se algum dia ativo do programa atual coincide com um dia ativo de outro programa ativo
                                    if DEBUG: print(j)
                                    dia_test = 1
                                    break
                            hI2 = "%02d%02d" % (Prog[i]['Hi'], Prog[i]['Mi'])
                            hF2 = "%02d%02d" % (Prog[i]['Hf'], Prog[i]['Mf'])
                            if (hInicio < hF2 or hF2=="0000") and (hI2 < hFim or hFim=="0000") and dia_test: #testar se os intervalos de tempo se intersetam
                                canal_test = 0
                                for j in range(12):
                                    if self.canais[j].isChecked() and Prog[i]['Canal'][j]:  #testar se algum canal ativo do programa atual coincide com um canal ativo de outro programa ativo 
                                        # sobreposição de canais&horas
                                        canal_test = 1
                                if canal_test: #se os programas tiverem conflitos nos canais guardar o indice do programa com que há conflito
                                    canal_list.append(i+1)
                                if self.fonte2.isChecked() != Prog[i]['Fonte']: #testar se a fonte do programa atual é a mesma do outro programa ativo (se não, há conflito)
                                    # sobreposição de fontes&horas
                                    fonte_list.append(i+1) #se os programas tiverem conflitos na fonte guardar o indice do programa com que há conflito
                    if not len(canal_list)==0 or not len(fonte_list)==0: #se existirem conflitos nos canais ou fonte
                        label = "AVISO\n\nPrograma atual tem conflitos com os seguintes:"
                        if not len(canal_list)==0:
                            if DEBUG: print(canal_list)
                            label += "\nnos canais:"
                            for k in range(len(canal_list)): label += " %d," % canal_list[k]
                            label = label[:-1] #imprimir os programas em que há conflito nos canais
                        if not len(fonte_list)==0:
                            if DEBUG: print(fonte_list)
                            label += "\nnas fontes:"
                            for k in range(len(fonte_list)): label += " %d," % fonte_list[k]
                            label = label[:-1] #imprimir os programas em que há conflito na fonte
                        label += "\n\nEfetue as alterações necessárias."
                        self.warningWindow.label.setText(label)
                        self.setEnabled(0) #desativar a main
                        self.warningWindow.show() #mostrar a janela de aviso de conflitos
                        return False    
            else: #se o utilizador não selecionar o(s) dia/s ou canais
                label = "AVISO\n\nNão preencheu"
                if dia_test==0:
                    label += " os dias"
                    if canal_test==0: label += " e"
                if canal_test==0: label += " os canais"
                label += ".\n\nEfetue as alterações necessárias."
                self.warningWindow.label.setText(label)
                self.setEnabled(0) #desativar a main
                self.warningWindow.show() #mostrar a janela de aviso de conflitos
                return False

        else:  #se a hora final for inferior à inicial
            self.warningWindow.label.setText("AVISO\n\nA hora de fim deve ser superior\nà hora de início.\n\nEfetue as alterações necessárias.")
            self.setEnabled(0)
            self.warningWindow.show()
            return False
        return True
    
    def on_off(self):
        k = self.progList.currentIndex()
        if not Prog[k]['A'] == int(self.ativo.isChecked()): # se o estado para que se quer mudar (on/off) não corresonder ao estado guardado
            if not self.comparar(): self.ativo.setChecked(0) #testar se o programa tem conflitos quando se tenta ativar
            else:
                Prog[k]['A'] = int(self.ativo.isChecked())
                # enviar ativo para o arduino
                ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
                ser.write('a'.encode('utf-8'))
                line=ser.readline().decode('utf-8').rstrip()
                if DEBUG: print(line)
                serialWrite(k)
                serialWrite(Prog[k]['A'])
        
        if self.ativo.isChecked():
            # setting background color to green
            self.ativo.setStyleSheet("background-color : green")
            self.ativo.setText("ON")
        else:
            # set background color back to red
            self.ativo.setStyleSheet("background-color : rgb(255,100,100)")
            self.ativo.setText("OFF")
           
    def createWarningWindow(self): #criar janela de aviso de conflitos
        self.warningWindow = subWindow()
        self.warningWindow.createWindow(500,250)
        self.warningWindow.setWindowTitle("Atenção")
        self.warningWindow.setStyleSheet("background-color : rgb(250,240,240)")
        # widgets
        self.warningWindow.label = QtWidgets.QLabel("AVISO",self.warningWindow)
        self.warningWindow.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.warningWindow.ok = QtWidgets.QPushButton("OK", self.warningWindow)
        self.warningWindow.ok.setStyleSheet("background-color : white")
        # posições
        self.warningWindow.label.resize(500,215)
        self.warningWindow.ok.setGeometry(200,215,100,30)
        # funções
        self.warningWindow.ok.clicked.connect(self.okFunction) #botão de OK
        
    def okFunction(self):
        self.progList.setCurrentIndex(lastProg) #voltar ao programa anterior
        self.setEnabled(1) #ativar a main
        self.warningWindow.hide() # esconder a anela de aviso de conflitos
    
    def createNotSavedWindow(self): #criar a janela de alterações não guardadas
        self.notSavedWindow = subWindow()
        self.notSavedWindow.createWindow(400,100)
        self.notSavedWindow.setWindowTitle("Alterações não guardadas")
        # widgets
        self.notSavedWindow.label = QtWidgets.QLabel("Pretende guardar as alterações efetuadas?", self.notSavedWindow)
        self.notSavedWindow.guardar = QtWidgets.QPushButton("Guardar", self.notSavedWindow)
        self.notSavedWindow.naoGuardar = QtWidgets.QPushButton("Não Guardar", self.notSavedWindow)
        self.notSavedWindow.cancelar = QtWidgets.QPushButton("Cancelar", self.notSavedWindow)
        # posições
        self.notSavedWindow.label.move(20,20)
        self.notSavedWindow.guardar.setGeometry(25,65,100,30)
        self.notSavedWindow.naoGuardar.setGeometry(150,65,100,30)
        self.notSavedWindow.cancelar.setGeometry(275,65,100,30)
        # funções
        self.notSavedWindow.guardar.clicked.connect(self.nSWguardar)
        self.notSavedWindow.naoGuardar.clicked.connect(self.nSWnaoGuardar)
        self.notSavedWindow.cancelar.clicked.connect(self.nSWcancelar)
        
    def nSWguardar(self): #botão de guardar as alterações ao programa anterior e ir para o novo programa
        self.setEnabled(1) 
        self.guardar.setChecked(0)
        self.guardarProg(lastProg)
        self.progFunction()
        self.notSavedWindow.hide()
        if self.varCloseEvent:
            if DEBUG: print(Prog[lastProg])
            self.close()

    def nSWnaoGuardar(self): #botão de ignorar as alterações não guardadas no programa anterior e ir para o novo programa
        self.setEnabled(1)
        self.guardar.setChecked(0)
        self.progFunction()
        self.notSavedWindow.hide()
        if self.varCloseEvent:
            if DEBUG: print(Prog[lastProg])
            self.close()
        
    def nSWcancelar(self): #botão de ignorar as alterações não guardadas no programa anterior e regressar a este
        self.progList.setCurrentIndex(lastProg)
        self.setEnabled(1)
        self.notSavedWindow.hide()
        self.varCloseEvent = 0
    
    def createInfoWindow(self,width,height): #criar a janela de alterações não guardadas
        self.infoWindow = subWindow()
        self.infoWindow.createWindow(width,height)
        self.infoWindow.setWindowTitle("Info")
        # widgets
        self.infoWindow.label1 = QtWidgets.QLabel(self.infoWindow)
        self.infoWindow.label2 = QtWidgets.QLabel(self.infoWindow)
        self.infoWindow.label1.setStyleSheet("font-size:10.75pt;")
        self.infoWindow.label2.setStyleSheet("font-size:10.75pt;")
        self.infoWindow.ok = QtWidgets.QPushButton("OK", self.infoWindow)
        # posições
        self.infoWindow.label1.move(20,10)
        self.infoWindow.ok.setGeometry(0,0,100,30)
        # funções
        self.infoWindow.ok.clicked.connect(self.okprogAtivos)
        
    def progAtivosFunction(self):
        self.setEnabled(0)
        nAtivos=0
        n10Ativos=1
        label=""
        label1=""
        for i in range(20):
            if Prog[i]['A']:
                nAtivos+=1
                if nAtivos == 11:
                    n10Ativos=2
                    label1=label
                    label=""
                label+="Programa %d:\n" %(i+1)
                label+="Dias: "
                for j in range(7):
                    if Prog[i]['D'][j]:
                        label+=self.diaName[j]+ ", "
                label+="\nInicio: %02d:%02d -- Fim: %02d:%02d" %(Prog[i]['Hi'], Prog[i]['Mi'],Prog[i]['Hf'],Prog[i]['Mf'])
                label+=" ---- Canais: "
                for j in range(12):
                    if Prog[i]['Canal'][j]:
                        label+= "%d, " %(j+1)
                label+="\nSensores: "
                for j in range(2):
                    if Prog[i]['Sensor'][j]:
                        label+= "%d, " %(j+1)
                label+=" ---- Fonte: "
                if Prog[i]['Fonte']:
                    label+="Bomba\n\n"
                else: label+="Torneira\n\n"
        self.createInfoWindow(450*n10Ativos,100+min(nAtivos*110,900))
        self.infoWindow.ok.move(int(450*n10Ativos/2)-50,60+min(nAtivos*110,900))
        if nAtivos > 10:
            self.infoWindow.label1.setText(label1)
            self.infoWindow.label2.setText(label)
            self.infoWindow.label2.move(470,10)
        else:
            self.infoWindow.label1.setText(label)
        
        self.infoWindow.show()
                
    def okprogAtivos(self):
        self.setEnabled(1) #ativar a main
        self.infoWindow.hide() # esconder a janela de info
            
    def debugFunction(self):
        print("DEBUG")
        receber_k(self.progList.currentIndex())
        debugTempo()
        debugSensores()
        self.setEnabled(0)
        self.warningWindow.show()


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 14pt;}" "QComboBox{font-size: 12pt;}" "QCheckBox{font-size: 12pt;}" "QRadioButton{font-size: 12pt;}" "QSpinBox{font-size: 12pt;}" "QPushButton{font-size: 12pt;}")

print("Inicializando...")
read_file()

ser = serial.Serial(dev_name, 9600, timeout=1) #Inicializar o Arduino
ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
initArduino() #Inicializar o Arduino

ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
ser.write('t'.encode('utf-8'))
initTempo() #Inicializar o tempo para o Arduino

for i in range(20): enviar(i) #Antes de encerrar o programa enviar as especificações dos programas para o Arduino

main = MainWindow()
main.show()  # Mostrar a janela

sys.exit(app.exec_()) # Fechar a aplicação e sair do programa