import serial
arduino = serial.Serial(port='COM10', baudrate=115200, timeout=.1)
arduino.write(b'H')

