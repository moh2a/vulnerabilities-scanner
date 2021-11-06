import queue

from PyQt5.QtCore import QObject, QThread, pyqtSignal
import socket

from PingTest import PingTest


class WorkerTest(QObject):
    finished = pyqtSignal()
    addText = pyqtSignal(str, str)

    def __init__(self, ip, ddos, xss, sqli, BF, parent=None):
        QThread.__init__(self, parent)
        self.ip = ip
        self.xss = xss
        self.sqli = sqli
        self.BF = BF
        self.ddos = ddos

    def run(self):
        self.addText.emit("Début du test.", "info")

        self.addText.emit("Adresse IP entrée : " + self.ip, "info")
        self.addText.emit("Ping : ", "black")
        resultPing = False
        self.Ping = PingTest(self.ip)
        # self.p = Process(target=Ping.test, args=(resultPing,))
        # self.p = Thread(target=Ping.test)
        self.Ping.start()
        resultPing = self.Ping.join()
        if resultPing:
            self.addText.emit("Réussi", "success")
        else:
            self.addText.emit("Echoué.", "alert")

        self.addText.emit("Fin du test.", "info")
        """Long-running task."""
        if self.ddos:
            self.addText.emit("Test DDOS indisponible pour le moment.", "alert")
        if self.xss:
            self.addText.emit("Test xss indisponible pour le moment.", "alert")
        if self.sqli:
            self.addText.emit("Test sqli indisponible pour le moment.", "alert")
        if self.BF:
            self.addText.emit("Test BF indisponible pour le moment.", "alert")
        self.finished.emit()

    def quit(self):
        print("ici")
        # self.Ping.
# 8.8.8.8
