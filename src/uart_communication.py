import struct
import serial
from crc import calcula_CRC

matr = b"\x04\x00\x03\x02"
codigos = {
    "tempInt": struct.pack("BBB", 0x01, 0x23, 0xC1) + matr,
    "tempRef": struct.pack("BBB", 0x01, 0x23, 0xC2) + matr,
    "leComando": struct.pack("BBB", 0x01, 0x23, 0xC3) + matr,
    "enviaContr": struct.pack("BBB", 0x01, 0x16, 0xD1) + matr,
    "enviaRef": struct.pack("BBB", 0x01, 0x16, 0xD2) + matr,
    "enviaESis": struct.pack("BBB", 0x01, 0x16, 0xD3) + matr,
    "enviaModo": struct.pack("BBB", 0x01, 0x16, 0xD4) + matr,
    "enviaEFun": struct.pack("BBB", 0x01, 0x16, 0xD5) + matr,
    "enviaTAmb": struct.pack("BBB", 0x01, 0x16, 0xD6) + matr,
    "liga": 0xA1,
    "desliga": 0xA2,
    "inicia": 0xA3,
    "cancela": 0xA4,
    "menu": 0xA5,
}

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


def verifyCRC(data):
    crc = struct.pack("H", calcula_CRC(data[:-2]))
    return not (crc == data[-2:])


def sendFloat(code: str, val: float) -> None:
    dataS = codigos[code] + struct.pack("f", val)
    dataS += struct.pack("H", calcula_CRC(dataS))

    ser.write(dataS)


def sendInt(code: str, val: int) -> None:
    dataS = codigos[code]
    dataS += struct.pack("i", val)
    dataS += struct.pack("H", calcula_CRC(dataS))

    ser.write(dataS)


def sendByte(code: str, val: bool) -> None:
    dataS = codigos[code]
    dataS += struct.pack("B", val)
    dataS += struct.pack("H", calcula_CRC(dataS))

    ser.write(dataS)


def getFloat(code: str) -> float:
    dataS = codigos[code]
    dataS += struct.pack("H", calcula_CRC(dataS))

    try:
        ser.readline()
    except:
        pass

    ser.write(dataS)
    dataR = ser.readline()

    while verifyCRC(dataR):
        ser.write(dataS)
        dataR = ser.readline()

    try:
        dataR = struct.unpack("<BBBfH", dataR)
    except struct.error:
        # print("Struct error")
        return getFloat(code)
    return dataR[-2]


def getInt(code: str) -> int:
    dataS = codigos[code]
    dataS += struct.pack("H", calcula_CRC(dataS))

    try:
        ser.readline()
    except:
        pass
    ser.write(dataS)
    dataR = ser.readline()

    while verifyCRC(dataR):
        # print(f"Erro: {dataR}")
        ser.write(dataS)
        dataR = ser.readline()
    try:
        dataR = struct.unpack("<BBBiH", dataR)
    except struct.error:
        # print("Struct error")
        return getInt(code)
    return dataR[-2]


def closeSerial():
    ser.close()
