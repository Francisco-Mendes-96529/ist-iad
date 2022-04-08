import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

 
k = 0

def leitura():
    print(k)
    time.sleep(0.2)
    if ser.inWaiting() <= 0:
        print("bufferinvalido")
    if ser.inWaiting() > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    ser.reset_input_buffer() 
    
while True:
    ser.write(bytes('0','utf-8'))
#     if k==0:
#         time.sleep(20)
    k += 1
    leitura()
    time.sleep(1)
    
    ser.write(bytes('9','utf-8'))
    k += 1
    leitura()
    time.sleep(1)
    
    ser.write(bytes('0','utf-8'))
    k += 1
    leitura()
    time.sleep(1)
    
    ser.write(bytes('1','utf-8'))
    k += 1
    leitura()
    time.sleep(1)
    