from PyQt5.QtCore import QObject, QThread, pyqtSignal
from Ddos import Ddos
from ListPages import ListPages
from PingTest import PingTest
from XSSTest import XSSTest
from BFTest import BFTest
from sqliAttackTest import sqliAttackTest

class WorkerTest(QObject):
    finished = pyqtSignal()
    addText = pyqtSignal(str, str)

    def __init__(self, ip,port, ddos, xss, sqli, BF,XXE, parent=None):
        QThread.__init__(self, parent)
        self.ip = ip
        self.port = port
        self.xss = xss
        self.sqli = sqli
        self.BF = BF
        self.XXE = XXE
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
            self.addText.emit("Début du XSS.", "info")
            self.addText.emit("XSS sur : " + self.ip + ":" + self.port, "info")
            self.xSSTest = XSSTest(pagesTable)
            self.xSSTest.start()
            resultxss = self.xSSTest.join()
            print("la", resultxss)
            if resultxss and (len(resultxss) > 0):
                self.addText.emit("L'attaque XSS a réussi", "success")
                self.addText.emit("Page(s) vulnérables : ", "info")
                for pages in resultxss:
                    self.addText.emit(pages + "\n", "black")
            else:
                self.addText.emit("L'attaque XSS a échouée. Aucune vulnérabilité rencontrée", "alert")
        if self.sqli:
            self.addText.emit("Début du SQLi.", "black")
            self.addText.emit("SQLi sur : " + self.ip + ":" + self.port, "info")
            self.sqliAttackTest_ = sqliAttackTest(pagesTable)
            self.sqliAttackTest_.start()
            resultsqli = self.sqliAttackTest_.join()
            if resultsqli and (len(resultsqli)>0):
                self.addText.emit("L'attaque SQL injection a réussi", "success")
                self.addText.emit("Page(s) vulnérables : ", "info")
                for pages in resultsqli:
                    self.addText.emit(pages + "\n", "black")
                print("Voici la liste des liens vulnérables : ", resultsqli)
            else: self.addText.emit("L'attaque SQL injection a échouée. Aucune vulnérabilité rencontrée", "alert")
        if self.BF:
            self.addText.emit("Début de la force brute.", "info")
            self.addText.emit("Force brute sur : " + self.ip + ":" + self.port, "info")
            self.BFtest = BFTest(pagesTable)
            self.BFtest.start()
            resultbf = self.BFtest.join()
            print("la", resultbf)
            if resultbf and (len(resultbf) > 0):
                self.addText.emit("L'attaque BF a réussi", "success")
                self.addText.emit("Utilisateur(s) et mot(s) de passe vulnérables : ", "info")
                for pages in resultbf:
                    self.addText.emit(pages + "\n", "black")
            else:
                self.addText.emit("L'attaque de force brute a échouée. Aucune vulnérabilité rencontrée", "alert")
        if self.ddos:
            self.addText.emit("Début du Ddos.", "info")
            self.addText.emit("Ddos sur : " + self.ip + ":" + self.port, "info")
            errorMax = 3 #au bout de 100 erreurs, le DDOS est réussi
            self.Ddos = Ddos(self.ip, self.port, errorMax)
            self.Ddos.start()
            ddosResult = self.Ddos.join()
            print("result : ", ddosResult["result"])
            if(ddosResult["result"] == "True"):
                self.addText.emit("Ddos réussi.", "success")
            else: self.addText.emit("Ddos echoué.", "alert")
            mess= "Nombre de threads utilisés : " + str(ddosResult['threads'])
            print("message : ", mess)
            self.addText.emit(mess, "info")
        self.finished.emit()

    def quit(self):
        print("ici")
