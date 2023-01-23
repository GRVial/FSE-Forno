from time import sleep
from uart_communication import *
import threading
import board
from adafruit_bme280 import basic as adafruit_bme280


class Dashboard(threading.Thread):
    sistema: bool
    funcionamento: bool
    modo: bool
    tempR: float
    tempI: float
    tempE: float

    def __init__(self):
        super().__init__()
        self.sistema = True
        self.funcionamento = True
        self.modo = False
        self.tempR = 0.0
        self.tempI = 0.0
        self.tempE = 0.0
        # self.event = event
        sendByte("enviaESis", 1)
        sendByte("enviaEFun", 1)
        sendByte("enviaModo", 0)
        i2c = board.I2C()
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    def run(self):
        while True:
            # if self.event.is_set():
            #     closeSerial()
            #     break
            com = getInt("leComando")
            self.tempR = getFloat("tempRef")
            self.tempI = getFloat("tempInt")
            self.tempE = self.bme280.temperature
            if com == codigos["liga"]:
                self.sistema = True
                sendByte("enviaESis", self.sistema)
            if com == codigos["desliga"]:
                self.sistema = False
                sendByte("enviaESis", self.sistema)
            if com == codigos["inicia"]:
                self.funcionamento = True
                sendByte("enviaEFun", self.funcionamento)
            if com == codigos["cancela"]:
                self.funcionamento = False
                sendByte("enviaEFun", 0)
            if com == codigos["menu"]:
                if self.modo:
                    self.modo = False
                    sendByte("enviaModo", 0)
                else:
                    self.modo = True
                    sendByte("enviaModo", 1)
            # sleep(0.5)
