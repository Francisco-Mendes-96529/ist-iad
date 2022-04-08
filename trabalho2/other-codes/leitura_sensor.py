import numpy as np
import serial
import PyQt5
import pyqtgraph as pg
import sys  
import os
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import time

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
    
ser = serial.Serial(dev_name, 9600)

# Função que testa se element é do tipo float
def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
    
# Classe da janela principal
class MainWindow(QtWidgets.QMainWindow):

    # Função que inicializa as propriedades da janela, dos botões e gráfico
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

#         MainWindow

        self.setWindowTitle("Trabalho 1 - Aquisição de dados e comunicação")
        # Dimensões
        self.setMinimumSize(1100,500)
        self.setMaximumSize(1100,500)
        # Posição no ecrã
        self.move(400,200)
        
#         Graph

        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(100,0,1000,500)  # (x, y, width, height)
        #Limites dos eixos
        self.graphWidget.setYRange(0,1023)
        self.graphWidget.setLimits(xMin = 0)
        #Label dos eixos
        self.graphWidget.setLabel('left', "Voltage (V)")
        self.graphWidget.setLabel('bottom', "Tempo (s)")
        
        self.x = [0]*200  # Lista com 200 pontos de tempo inicializados a 0
        self.y = [0]*200  # Lista com 200 pontos de voltagem inicializados a 0
        pen = pg.mkPen(color=(255, 0, 0))  # Cor da linha 
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        
#         Button Start
        self.bStart = QtWidgets.QPushButton("Start",self)
        self.bStart.clicked.connect(self.fStart)  # Quando se clica no botão chama a função fStart
        self.bStart.setGeometry(0,50,100,75)  
        self.bStart.setStyleSheet("background-color: green; color: white;font-size:21px")
        
#         Button Stop
        self.bStop = QtWidgets.QPushButton("Stop",self)
        self.bStop.setGeometry(0,175,100,75)
        self.bStop.clicked.connect(self.fStop)  # Quando se clica no botão chama a função fStop
        self.bStop.setStyleSheet("background-color: red; color: white;font-size:21px")

#         Caixa de texto de comando
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(0, 325,100,50)
        self.textbox.returnPressed.connect(self.fArduino)  # Quando se clica no Enter chama a função fArduino
        self.textbox.setMaxLength(1);  # Definir tamanho máximo do comando a enviar
        self.textbox.setStyleSheet("font-size:21px")  # Tamanho da fonte = 21 pixeis
        self.textbox.setAlignment(QtCore.Qt.AlignCenter)  # Alinhar texto no meio da textbox
        
#         Botão de comando
        self.arduino = QtWidgets.QPushButton("Enviar",self)
        self.arduino.clicked.connect(self.fArduino)  # Quando se clica no botão chama a função fArduino
        self.arduino.setGeometry(0,375,100,50)
        self.arduino.setStyleSheet("background-color: rgb(255,192,203);font-size:21px")
           
        # Definir um cronómetro
        self.timer = QtCore.QTimer()  
        
    def fStart(self):
        if not self.timer.isActive():  # Verificar se o cronómetro ainda não está ativo
            self.timer.timeout.connect(self.update_plot)  # Definir qual é a função que chama 
            self.timer.setInterval(50)#ms  # Definir de quanto em quanto tempo chama a função 
            self.timer.start()
        
    def fStop(self):    
        self.timer.stop()
        
    def fArduino(self):
        if self.timer.isActive():
            self.timer.stop()
        self.texto = self.textbox.text()  # Ler o texto da textbox
        ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
        ser.write(bytes(self.texto,'utf-8'))  # Traduzir o comando para bytes
        time.sleep(0.03)  # Tempo de espera entre escrita e leitura
        
        print("\nResultado do comando:")
        # Verificar se há algo escrito no buffer pelo Arduino
        if ser.inWaiting() > 0:
            line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
            print(line)
        else:
            print("buffer invalido")
        
    def update_plot(self):
        number = "0"
        ser.reset_input_buffer()
        ser.write(bytes("0",'utf-8'))  # Enviar ao Arduino o comando de leitura
        time.sleep(0.03)
        if ser.inWaiting() > 0:
            number = ser.readline().decode('utf-8').rstrip()
        else:
            print("buffer invalido")
            
        if is_float(number):  # Testar se valor lido pelo Arduino é float
            print(number)
            
            self.x = self.x[1:]  # Remove the first x element.
            self.x.append(self.x[-1] + 0.05)  # Add a new value 0.05s higher than the last.

            self.y = self.y[1:]  # Remove the first y element
            self.y.append(float(number))  # Add the new value.

            self.data_line.setData(self.x, self.y)  # Update the data.
            self.graphWidget.setYRange(0,1023)
        else:
            print("Not a float")
            print(number)

app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()  # Mostrar a janela
sys.exit(app.exec_())  # Fechar a aplicação e sair do programa