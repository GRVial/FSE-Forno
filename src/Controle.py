import RPi.GPIO as GPIO
from time import sleep
from uart_communication import *
from simple_pid import PID
import threading
from Dashboard import Dashboard


class Controle(threading.Thread):
    pid: PID
    db: Dashboard
    sinal_resistor: float
    sinal_ventoinha: float
    kp: float
    ki: float
    kd: float
    kill: bool

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.kp = 30.0
        self.ki = 0.2
        self.kd = 400.0
        self.kill = False
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
        self.pid.output_limits = (-100, 100)

    def clamp(self, l, r, x):
        return min(r, max(l, x))

    def changeTunings(self, kp: float, ki: float, kd: float):
        self.pid.tunings = (kp, ki, kd)
        print(f"Kp, Ki e Kd definidos para: {kp, ki, kd}")

    def run(self):
        while not self.kill:
            if self.db.sistema and self.db.funcionamento:
                self.pid.setpoint = self.db.tempR
                pid_out = self.pid(self.db.tempI)
                if pid_out > 0:
                    self.sinal_resistor = pid_out
                    self.sinal_ventoinha = 0
                else:
                    self.sinal_resistor = 0
                    self.sinal_ventoinha = self.clamp(40, 100, -pid_out)
                    pid_out = -self.sinal_ventoinha
                # print('TempRef: ', self.db.tempR, '\tTempInt: ', self.db.tempI, '\tsinal_resistor: ', "%.2f" % self.sinal_resistor, '\tSinal_ventoinha: ', "%.2f" % self.sinal_ventoinha, sep=None)
                # print('pid: ', "%.2f" % pid_out, '\n', sep=None)
                self.resistor.ChangeDutyCycle(self.sinal_resistor)
                self.ventoinha.ChangeDutyCycle(self.sinal_ventoinha)
                sendInt("enviaContr", int(pid_out))
                sleep(5)
        self.resistor.ChangeDutyCycle(0.0)
        self.ventoinha.ChangeDutyCycle(0.0)
        GPIO.cleanup()

    def kill_thread(self):
        self.kill = True
