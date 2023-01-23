from threading import Thread
import Dashboard
import Controle


class Menu(Thread):
    kill: bool
    db: Dashboard
    c: Controle

    def __init__(self, db: Dashboard, c: Controle):
        super().__init__()
        self.kill = False
        self.db = db
        self.c = c

    def run(self):
        while not self.kill:
            print("[1] Mudar valores Kp, Ki, Kd")
            print("[2] Mudar Referencia")
            print(f"Temperatura Interna: {self.db.tempI}")
            print(f"Temperatura de Referencia: {self.db.tempR}")
            print(f"Temperatura Ambiente: {self.db.tempE}")
            op = input()
            if op == "1":
                kp, ki, kd = [float(i) for i in input("Digite: <Kp Ki Kd>").split()]
                self.c.changeTunings(kp, ki, kd)
            if op == "2":
                self.db.tempR = float(input("Digite a temperatura: "))

    def kill_thread(self):
        self.kill = True
        print("ENTER para encerrar")
