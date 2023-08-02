import serial
import time
arduino = serial.Serial(port='COM10', baudrate=115200, timeout=.1)
while True:
    arduino.write(b'H')