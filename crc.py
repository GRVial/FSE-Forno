# import crcmod

# # Define the data string
# data = "Hello, CRC!"

# # Create a new crc function using the CRC-16-CCITT polynomial
# crc16 = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF, xorOut=0x0000)

# # Calculate the CRC value for the data
# crc = crc16(data.encode())

# # Print the calculated CRC value
# print("Calculated CRC:", hex(crc))

# # Append the calculated CRC value to the data
# data_with_crc = data.encode() + crc.to_bytes(2, byteorder='big')

# # Verify the data using the same crc function
# is_valid = crc16(data_with_crc[:-2]) == crc

# # Print the result of the verification
# print("Data is valid:", is_valid)

import crcmod

# Define the data string
data = "Hello, IBM CRC!"

# Create a new crc function using the IBM polynomial
crc16_ibm = crcmod.mkCrcFun(0x8005, initCrc=0xFFFF, xorOut=0x0000, rev=True)

# Calculate the CRC value for the data
crc = crc16_ibm(data.encode())

# Print the calculated CRC value
print("Calculated CRC:", hex(crc))
