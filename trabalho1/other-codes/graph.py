import numpy as np
import serial
import PyQt5
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
from random import randint
import time

if os.path.exists('/dev/ttyACM0'):
    dev_name = '/dev/ttyACM0'
if os.path.exists('/dev/ttyACM1'):
    dev_name = '/dev/ttyACM1'
if os.path.exists('/dev/ttyACM2'):
    dev_name = '/dev/ttyACM2'

ser = serial.Serial(dev_name, 9600)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

#         MainWindow
        self.setWindowTitle("Trabalho 1 - Aquisição de dados e comunicação")
        self.setMinimumSize(1100,500)
        self.setMaximumSize(1100,500)

#         Graph
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(100,0,1000,500)
        self.graphWidget.setYRange(0,5)
        self.graphWidget.setLimits(xMin = 0)
#         Button Start
        self.bStart = QtWidgets.QPushButton("Start",self)
        self.bStart.clicked.connect(self.fStart)
        self.bStart.setGeometry(0,50,100,75)
        self.bStart.setStyleSheet("background-color: green; color: white;font-size:21px")
        
#         Button Stop
        self.bStop = QtWidgets.QPushButton("Stop",self)
        self.bStop.setGeometry(0,175,100,75)
        self.bStop.clicked.connect(self.fStop)
        self.bStop.setStyleSheet("background-color: red; color: white;font-size:21px")
        
#         Axis Plot
        self.x = [0]*200  # 100 time points
        self.y = [0]*200  # 100 data points
        # plot data: x, y values
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)        
        self.timer = QtCore.QTimer()
        
        self.textbox =QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(0, 325,100,50)
        self.textbox.returnPressed.connect(self.fArduino)
        self.textbox.setMaxLength(1);
        self.textbox.setStyleSheet("font-size:21px")
        self.textbox.setAlignment(QtCore.Qt.AlignCenter)
        
        self.arduino = QtWidgets.QPushButton("Enviar",self)
        self.arduino.clicked.connect(self.fArduino)
        self.arduino.setGeometry(0,375,100,50)
        self.arduino.setStyleSheet("background-color: rgb(255,192,203);font-size:21px")
        
    def fArduino(self):
        self.texto = self.textbox.text()
        ser.reset_input_buffer()
#         ser.write(bytes('0','utf-8'))
        ser.write(bytes(self.texto,'utf-8'))
        time.sleep(0.03)
        if ser.inWaiting() <= 0:
            print("bufferinvalido")
        if ser.inWaiting() > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
        
    def fStart(self):
        if not self.timer.isActive():
            self.timer.setInterval(50)
            self.timer.timeout.connect(self.update_plot)
            self.timer.start()
        
    def fStop(self):    
        self.timer.stop()
        
    def update_plot(self):
        number = 0
        ser.reset_input_buffer()
#         ser.write(bytes('0','utf-8'))
        ser.write(bytes("0",'utf-8'))
        time.sleep(0.03)
        if ser.inWaiting() <= 0:
            print("bufferinvalido")
        if ser.inWaiting() > 0:
            number = float(ser.readline().decode('utf-8').rstrip())
        
        if isinstance(number,(float,int)):
            print(number)
            
            self.x = self.x[1:]  # Remove the first x element.
            self.x.append(self.x[-1] + 0.05)  # Add a new value 1 higher than the last.

            self.y = self.y[1:]  # Remove the first y element
            self.y.append(float(number))  # Add a new value.

            self.data_line.setData(self.x, self.y)  # Update the data.
            self.graphWidget.setYRange(0,5)
        else:
            print("not float")
            print(number)




app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
