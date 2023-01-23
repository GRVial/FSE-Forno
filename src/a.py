import RPi.GPIO as GPIO
import time
from uart_communication import *
from simple_pid import PID

def clamp(l, r, x):
    return min(r, max(l, x))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)    #resist
GPIO.setup(24, GPIO.OUT)    #vent

resistor = GPIO.PWM(23, 1000)
ventoinha = GPIO.PWM(24, 1000)
ventoinha.start(0.0)
resistor.start(0.0)

pid = PID(30., 0.2, 400., sample_time=0.5)
TR = 50.0

while True:
    TR = getFloat('tempRef')
    temp = getFloat('tempInt')
    pid.setpoint = TR
    pid_curr = pid(temp)

    print('TempRef: ', TR, '\tTempInt: ', temp, sep=None)
    print('pid: ', pid_curr, sep=None)

    sinal = int(clamp(-100., 100., pid_curr))
    resistor.ChangeDutyCycle(clamp(0., 100., pid_curr))
    ventoinha.ChangeDutyCycle(clamp(0., 100., -pid_curr))

    sendInt('enviaContr', sinal)

    time.sleep(0.5)