import serial
import time
from threading import Timer

ser = serial.Serial('/dev/ttyACM0', 9600)
 
k = 0

def leitura():
    print(k)
    ser.write(bytes('0','utf-8'))
    time.sleep(0.2)
    if ser.inWaiting() <= 0:
        print("bufferinvalido")
    if ser.inWaiting() > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    ser.reset_input_buffer() 
    
while True:
    k += 1
    leitura()
    time.sleep(1)
    
