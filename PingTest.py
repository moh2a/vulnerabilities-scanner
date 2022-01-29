import os
from threading import Thread


class PingTest(Thread):
    def __init__(self, ip):
        # Call the Thread class's init function
        Thread.__init__(self)
        self.ip = ip


    def run(self):
        ping = os.system("ping -n 1 " + self.ip)
        print("ping", ping)
        if ping == 0:
            self.resultPing = True

        else:
            self.resultPing = Falses

    def join(self):
        Thread.join(self)
        return self.resultPing
