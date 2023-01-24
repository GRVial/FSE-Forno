from Dashboard import Dashboard
from Controle import Controle
from Menu import Menu
from time import sleep
from datetime import datetime
import os


def write_log(temp_int, temp_ref, temp_ext, sinal_v, sinal_r):
    if not os.path.isfile("./log.csv"):
        with open("log.csv", "a", encoding="UTF8") as f:
            f.write(
                "data,temp_interna,temp_referencia,temp_externa,acionamento_ventoinha,acionamento_resistor\n"
            )
    with open("log.csv", "a", encoding="UTF8") as f:
        f.write(
            f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")},{temp_int:.2f},{temp_ref:.2f},{temp_ext:.2f},{sinal_v:.2f},{sinal_r:.2f}\n'
        )


def main():
    try:
        db = Dashboard()
        db.start()
        c = Controle(db)
        c.start()
        m = Menu(db, c)
        m.start()

        while True:
            write_log(db.tempI, db.tempR, db.tempE, c.sinal_ventoinha, c.sinal_resistor)
            sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando!")
        db.kill_thread()
        db.join()
        c.kill_thread()
        c.join()
        m.kill_thread()
        m.join()


if __name__ == "__main__":
    main()
