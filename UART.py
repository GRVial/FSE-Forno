import serial

# Open the serial port
ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

# Send data to the serial port
ser.write(b'Hello, UART!')

# Read data from the serial port
data = ser.readline()

# Print the received data
print(data)

# Close the serial port
ser.close()
