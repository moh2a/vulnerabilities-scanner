from PyQt5.QtCore import QObject, QThread, pyqtSignal
from Ddos import Ddos
from ListPages import ListPages
from PingTest import PingTest


class WorkerTest(QObject):
    finished = pyqtSignal()
    addText = pyqtSignal(str, str)

    def __init__(self, ip,port, ddos, xss, sqli, BF, parent=None):
        QThread.__init__(self, parent)
        self.ip = ip
        self.port = port
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

        # lancement de la tache de listing des pages :

        self.addText.emit("Début du listing des pages.", "info")
        self.addText.emit("Listing sur : " + self.ip+":"+self.port, "info")
        resultPing = False
        self.ListPages = ListPages(self.ip, self.port)
        self.ListPages.start()
        pagesTable = self.ListPages.join()
        self.addText.emit("Pages trouvées : \n", "success")
        for pages in pagesTable:
            self.addText.emit(pages+"\n", "black")
        if self.xss:
            self.addText.emit("Test xss indisponible pour le moment.", "alert")
        if self.sqli:
            self.addText.emit("Test sqli indisponible pour le moment.", "alert")
        if self.BF:
            self.addText.emit("Test BF indisponible pour le moment.", "alert")
        if self.ddos:
            self.addText.emit("Début du Ddos.", "info")
            self.addText.emit("Ddos sur : " + self.ip + ":" + self.port, "info")
            errorMax = 5 #au bout de 100 erreurs, le DDOS est réussi
            self.Ddos = Ddos(self.ip, self.port, errorMax)
            self.Ddos.start()
            ddosResult = self.Ddos.join()
            if(ddosResult): self.addText.emit("Ddos réussi.", "success")
            else : self.addText.emit("Ddos echoué.", "alert")
        self.finished.emit()

    def quit(self):
        print("ici")
