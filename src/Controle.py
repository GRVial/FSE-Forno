import RPi.GPIO as GPIO
from time import sleep
from uart_communication import *
from simple_pid import PID
import threading
from Dashboard import Dashboard



class Controle(threading.Thread):
    pid : PID
    db : Dashboard
    sinal_resistor : float
    sinal_ventoinha : float
    def __init__(self, db):
        super().__init__()
        # self.event = event
        self.db = db
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT)  # resist
        GPIO.setup(24, GPIO.OUT)  # vent
        self.resistor = GPIO.PWM(23, 1000)
        self.ventoinha = GPIO.PWM(24, 1000)
        self.sinal_resistor = 0.0
        self.sinal_ventoinha = 0.0
        self.ventoinha.start(0.0)
        self.resistor.start(0.0)
        self.pid = PID(30.0, 0.2, 400.0, sample_time=0.5)

    def clamp(self, l, r, x):
        return min(r, max(l, x))

    def run(self):
        while True:
            # if self.event.is_set():
            #         break
            if self.db.sistema and self.db.funcionamento:
                print('dentro')
                self.pid.setpoint = self.db.tempR
                pid_out = self.pid(self.db.tempI)
                sinalRef = int(self.clamp(-100.0, 100.0, pid_out))
                self.sinal_resistor = self.clamp(0.0, 100.0, pid_out)
                self.sinal_ventoinha =self.clamp(0.0, 100.0, -pid_out)
                print('TempRef: ', self.db.tempR, '\tTempInt: ', self.db.tempI, '\tsinal_resistor: ', self.sinal_resistor, sep=None)
                print('pid: ', pid_out, sep=None)
                self.resistor.ChangeDutyCycle(self.sinal_resistor)
                self.ventoinha.ChangeDutyCycle(self.sinal_ventoinha)
                sendInt('enviaContr', sinalRef)
                sleep(1)
