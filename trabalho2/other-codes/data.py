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

today = time.strftime("%w, %H:%M:%S")
print(today)

while True:
    time.sleep(1)  # Tempo de espera entre escrita e leitura

    weekDay = time.strftime("%w")
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(bytes(weekDay,'utf-8'))
    time.sleep(0.03)  # Tempo de espera entre escrita e leitura
            
    print("\nResultado do comando:")
    # Verificar se há algo escrito no buffer pelo Arduino
    if ser.inWaiting() > 0:
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        print(line)
    else:
        print("buffer invalido")
