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

today = time.strftime("%w, %H:%M:%S\n")
print(today)

weekDay = time.strftime("%w")

print("\nResultado do comando:")
# Verificar se há algo escrito no buffer pelo Arduino
j=0
while True:
    ser.reset_input_buffer()  # Reset do buffer para dar a ordem ao Arduino
    ser.write(today.encode('utf-8'))
    j += 1
#     print(j)
    time.sleep(0.03)
    if ser.inWaiting() > 0:
        line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
        print(line)
        print(j)
    time.sleep(1)
#         break
#     else:
#         print("buffer invalido")

