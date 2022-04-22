import numpy as np
import serial
import PyQt5
import pyqtgraph as pg
import sys  
import os
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot

def initArduino():
    while True:
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
        
def enviar(int k):
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['A'].encode('utf-8'))
    for j in range(7):
        ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
        ser.write(Prog[k]['D'][j].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Hi'].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Mi'].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Hf'].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Mf'].encode('utf-8'))
    for j in range(12):
        ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
        ser.write(Prog[k]['Canais'][j].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Fonte'].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Sensor'][0].encode('utf-8'))
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(Prog[k]['Sensor'][1].encode('utf-8'))

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
    
Prog = [{'A':0, 'D':[0,0,0,0,0,0,0], "Hi":0, "Mi":0, "Hf":0, "Mf":0, "Canal":[0,0,0,0,0,0,0,0,0,0,0,0], "Fonte":0, "Sensor":[0,0]} for i in range(20)]

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
        self.horaInicial = QtWidgets.QSpinBox(self)
        self.minInicial = QtWidgets.QSpinBox(self)
        self.horaFinal = QtWidgets.QSpinBox(self)
        self.minFinal = QtWidgets.QSpinBox(self)
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
        self.guardar = QtWidgets.QPushButton("Guardar",self)
        self.guardar.setGeometry(760,420,100,50)
        self.guardar.clicked.connect(self.guardarFunction)
        self.ativo = QtWidgets.QPushButton("OFF",self)
        self.ativo.setCheckable(True)
        self.ativo.setGeometry(680,420,70,50)
        self.ativo.clicked.connect(self.on_off)
        self.ativo.toggled.connect(self.on_off)
        self.ativo.setStyleSheet("background-color : rgb(255,100,100)") # set background color to red
        
# After Functions
        self.progFunction()
        
# Funções        
    def progFunction(self):
        k = self.progList.currentIndex()
        self.ativo.setChecked(Prog[k]['A'])
        for i in range(7):
            self.dia[i].setCheckState(Prog[k]['D'][i])
        self.horaInicial.setValue(Prog[k]['Hi'])
        self.minInicial.setValue(Prog[k]['Mi'])
        self.horaFinal.setValue(Prog[k]['Hf'])
        self.minFinal.setValue(Prog[k]['Mf'])
        for i in range(12):
            self.canais[i].setCheckState(Prog[k]['Canal'][i])
        self.fonte1.setChecked(not Prog[k]['Fonte'])
        self.fonte2.setChecked(Prog[k]['Fonte'])
        self.sensor[0].setCheckState(Prog[k]['Sensor'][0])
        self.sensor[1].setCheckState(Prog[k]['Sensor'][1])
        enviar(k)
        
    def guardarFunction(self):
        k = self.progList.currentIndex()
        Prog[k]['A'] = self.ativo.isChecked()
        for i in range(7):
            Prog[k]['D'][i] = self.dia[i].checkState()
        Prog[k]['Hi'] = self.horaInicial.value()
        Prog[k]['Mi'] = self.minInicial.value()
        Prog[k]['Hf'] = self.horaFinal.value()
        Prog[k]['Mf'] = self.minFinal.value()
        for i in range(12):
            Prog[k]['Canal'][i] = self.canais[i].checkState()
        Prog[k]['Fonte'] = self.fonte2.isChecked()
        Prog[k]['Sensor'][0] = self.sensor[0].checkState()
        Prog[k]['Sensor'][1] = self.sensor[1].checkState()
        
    def on_off(self):
        if self.ativo.isChecked():
            # setting background color to green
            self.ativo.setStyleSheet("background-color : green")
            self.ativo.setText("ON")
        else:
            # set background color back to red
            self.ativo.setStyleSheet("background-color : rgb(255,100,100)")
            self.ativo.setText("OFF")
   

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 14pt;}" "QComboBox{font-size: 12pt;}" "QCheckBox{font-size: 12pt;}" "QRadioButton{font-size: 12pt;}" "QSpinBox{font-size: 12pt;}" "QPushButton{font-size: 12pt;}")

ser = serial.Serial(dev_name, 9600, timeout=1)
ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
initArduino()

ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
ser.write('e'.encode('utf-8'))
receber()

main = MainWindow()
main.show()  # Mostrar a janela
sys.exit(app.exec_()) # Fechar a aplicação e sair do programa