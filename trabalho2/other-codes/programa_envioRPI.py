# import numpy as np
import serial
# import PyQt5
# import pyqtgraph as pg
import sys  
import os
# from PyQt5 import QtWidgets, QtCore
# from pyqtgraph import PlotWidget, plot
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
    
def initArduino():
    start = time.time()
    while True:
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        if line=="Arduino is ready":
            print(line)
            stop = time.time()
            print(stop-start)
            break
        
def receber():
    for i in range(20):
        for j in range(7):
            Prog[i]['D'][j] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['H'] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['M'] = int(ser.readline().decode('utf-8').rstrip())
        for j in range(12):
            Prog[i]['Canal'][j] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Fonte'] = int(ser.readline().decode('utf-8').rstrip())
        Prog[i]['Sensor'] = int(ser.readline().decode('utf-8').rstrip())
        
        
Prog = [{'D':[0,0,0,0,0,0,0], "H":0, "M":0, "Canal":[0,0,0,0,0,0,0,0,0,0,0,0], "Fonte":0, "Sensor":0} for i in range(20)]

ser = serial.Serial(dev_name, 9600, timeout=1)

ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
initArduino()

for k in range(20):
    print("Progama",k)
    print(Prog[k])
# print("Progama",3)
# print(Prog[2])

ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
ser.write('e'.encode('utf-8'))
receber()

for k in range(20):
    print("Progama",k)
    print(Prog[k])
# print("Progama",3)
# print(Prog[2])
