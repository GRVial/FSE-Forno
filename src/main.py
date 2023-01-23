from Dashboard import Dashboard
from Controle import Controle
from threading import Event
import signal
import sys
from time import sleep
from datetime import datetime
import os


def write_log(temp_int, temp_ref, temp_ext, sinal_v, sinal_r):
    if not os.path.isfile("./log.csv"):
        with open("log.csv", "a", encoding="UTF8") as f:
            f.write(
                "data,temp_interna,temp_referencia,temp_externa,temp_usuario,acionamento_ventoinha,acionamento_resistor\n"
            )
    with open("log.csv", "a", encoding="UTF8") as f:
        f.write(
            f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")},{temp_int:.2f},{temp_ref:.2f},{temp_ext:.2f},(temp_usuario),{sinal_v},{sinal_r}\n'
        )


def main():
    # def signal_handler(sig, frame):
    #     print("\nSIGINT recebido")
    #     event.set()
    #     db.join()
    #     sys.exit(0)

    # event = Event()
    db = Dashboard()
    db.start()
    c = Controle(db)
    c.start()
    # signal.signal(signal.SIGINT, signal_handler)
    while True:
        write_log(db.tempI, db.tempR, db.tempE, c.sinal_ventoinha, c.sinal_resistor)
        sleep(1)

if __name__ == "__main__":
    main()
