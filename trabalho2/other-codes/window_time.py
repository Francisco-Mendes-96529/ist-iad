import numpy as np
import serial
import PyQt5
import pyqtgraph as pg
import sys  
import os
from PyQt5 import QtWidgets, QtCore
import time

#DEBUG
DEBUG = True

# Funções de comunicação com o Arduino
def serialWrite(var):
    ser.write((str(var)+"\n").encode('utf-8'))

def initArduino():
    while True:
#         serial.write('i'.encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        if line=="Arduino is ready":
            print(line)
            break
        
def receber():
    for i in range(20):
        Prog[i]['A'] = int(ser.readline().decode('utf-8').rstrip())
        for j in range(7):
            Prog[i]['D'][j] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Hi'] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Mi'] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Hf'] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Mf'] = int(ser.readline().decode('utf-8').rstrip())
        for j in range(12):
            Prog[i]['Canal'][j] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Fonte'] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Sensor'][0] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Sensor'][1] = int(ser.readline().decode('utf-8').rstrip())
        
def enviar(k):
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('r'.encode('utf-8'))
    print(ser.readline().decode('utf-8').rstrip())
    serialWrite(k)
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
        
def receber_k(k):
    print("DEBUG")
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('k'.encode('utf-8'))
    serialWrite(k)
    print(ser.readline().decode('utf-8').rstrip())
    for i in range(27):
        print(ser.readline().decode('utf-8').rstrip())

def initTempo():
    today = time.strftime("%w, %H:%M:%S")
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(today.encode('utf-8'))
    while True:
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        if line=="LEITURA VALIDA":
            print(line)
            break
        elif line=="LEITURA INVALIDA":
            today = time.strftime("%w, %H:%M:%S")
            ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
            ser.write(today.encode('utf-8'))

def debugTempo():
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write('T'.encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
    print(line)


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
lastProg = 0
# Lista de 20 dicionários (programas)
Prog = [{'A':0, 'D':[0,0,0,0,0,0,0], "Hi":0, "Mi":0, "Hf":0, "Mf":0, "Canal":[0,0,0,0,0,0,0,0,0,0,0,0], "Fonte":0, "Sensor":[0,0]} for i in range(20)]

# SpinBox com 2 dígitos
class DoubleDigitSpinBox(QtWidgets.QSpinBox):
    def __init__(self, *args):
       QtWidgets.QSpinBox.__init__(self, *args)

    def textFromValue(self, value):
       return "%02d" % value

# classe de janelas secundárias
class subWindow(QtWidgets.QWidget):
    def createWindow(self,width,height):
        parent = None
        super(subWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
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


# Drop down list Programas
        self.progList = QtWidgets.QComboBox(self)
        self.progList.addItems([str(i+1) for i in range(20)])
        self.progList.setGeometry(490, 0, 50, 50)
        self.progList.currentIndexChanged.connect(self.progFunction)
        
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
        
# Checkboxes dias
        diaName = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.dia = [QtWidgets.QCheckBox(diaName[i], self)for i in range(7)]
        for i in range(7):
            self.dia[i].setGeometry(75, 50*i+100, 110, 50)
        
# Checkboxes canais
        self.canais = [QtWidgets.QCheckBox(str(i+1), self)for i in range(12)]
        for i in range(6):
            self.canais[i].setGeometry(710, 50*i+100, 100, 50)
            self.canais[i+6].setGeometry(790, 50*i+100, 100, 50)

# Checkboxes sensores
        self.sensor = [QtWidgets.QCheckBox(str(i+1), self)for i in range(2)]
        self.sensor[0].setGeometry(380, 280, 100, 50)
        self.sensor[1].setGeometry(480, 280, 100, 50)
        
# Selecionar Fonte
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

# Botões Guardar e Ativo
        self.guardar = QtWidgets.QPushButton("Editar",self)
        self.guardar.setCheckable(True)
        self.guardar.setGeometry(760,420,100,50)
        self.guardar.toggled.connect(self.guardarFunction)
        self.ativo = QtWidgets.QPushButton("OFF",self)
        self.ativo.setCheckable(True)
        self.ativo.setGeometry(680,420,70,50)
        self.ativo.toggled.connect(self.on_off)
        
# Botão debug
        if DEBUG:
            self.debugButton = QtWidgets.QPushButton("Debug",self)
            self.debugButton.clicked.connect(self.debugFunction)
        
# After Functions
        self.progFunction()
        self.createNotSavedWindow()
        self.varCloseEvent = 0 # = 1 quando estamos a editar e tentamos fechar a mainWindow
        
# Funções
    def closeEvent(self, event):
        if self.notSavedWindow.isVisible():
            event.ignore()
        elif self.guardar.isChecked():
            self.varCloseEvent = 1
            self.setEnabled(0)
            self.notSavedWindow.show()
            event.ignore()
        else:
            event.accept()
        
    def progFunction(self):
        global lastProg
        k = self.progList.currentIndex()
        if self.guardar.isChecked():
            self.setEnabled(0)
            self.notSavedWindow.show()
        else:
            lastProg = k
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
            
    def guardarFunction(self):
        if self.guardar.isChecked():
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
        else:
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
        # Guardar programa
            k = self.progList.currentIndex()
            if  k == lastProg and not self.varCloseEvent:
                self.guardarProg(k)
                
    def guardarProg(self,index):
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

        
    def on_off(self):
        k = self.progList.currentIndex()
        if not Prog[k]['A'] == int(self.ativo.isChecked()):
            Prog[k]['A'] = int(self.ativo.isChecked())
            # enviar ativo para o arduino
            ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
            ser.write('a'.encode('utf-8'))
            print(ser.readline().decode('utf-8').rstrip())
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
           
    def createNotSavedWindow(self):
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
        
    def nSWguardar(self):
        self.setEnabled(1)
        self.guardar.setChecked(0)
        self.guardarProg(lastProg)
        self.progFunction()
        self.notSavedWindow.hide()
        if self.varCloseEvent:
            if DEBUG: print(Prog[lastProg])
            self.close()

    def nSWnaoGuardar(self):
        self.setEnabled(1)
        self.guardar.setChecked(0)
        self.progFunction()
        self.notSavedWindow.hide()
        if self.varCloseEvent:
            if DEBUG: print(Prog[lastProg])
            self.close()
        
    def nSWcancelar(self):
        self.progList.setCurrentIndex(lastProg)
        self.setEnabled(1)
        self.notSavedWindow.hide()
        
        
    def debugFunction(self):
        receber_k(self.progList.currentIndex())
        debugTempo()


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 14pt;}" "QComboBox{font-size: 12pt;}" "QCheckBox{font-size: 12pt;}" "QRadioButton{font-size: 12pt;}" "QSpinBox{font-size: 12pt;}" "QPushButton{font-size: 12pt;}")

ser = serial.Serial(dev_name, 9600, timeout=1)
ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
initArduino()

ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
ser.write('e'.encode('utf-8'))
receber()

ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
ser.write('t'.encode('utf-8'))
initTempo()

main = MainWindow()
main.show()  # Mostrar a janela
sys.exit(app.exec_()) # Fechar a aplicação e sair do programa