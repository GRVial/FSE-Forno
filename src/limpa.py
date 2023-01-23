import serial

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
while True:
    ser.write(b'temperatura')
    ser.write(b'\x01#\xc1\x02\x02\x00\x00\x8a:')