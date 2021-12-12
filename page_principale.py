# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\imran\PycharmProjects\pythonProject\page_principale.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import ipaddress
from WorkerTest import WorkerTest


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.textColor = {}
        self.textColor["end"] = "</font><br>"
        self.textColor["alert"] = "<font color=#B73B15>"
        self.textColor["info"] = "<font color=#1595B7>"
        self.textColor["black"] = "<font color=#000>"
        self.textColor["success"] = "<font color=#43B715>"
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(554, 348)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 1, 0, 1, 5)
        self.displayOutput = QtWidgets.QTextBrowser(self.centralwidget)
        self.displayOutput.setObjectName("displayOutput")
        self.gridLayout_2.addWidget(self.displayOutput, 0, 0, 1, 5)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 4, 4, 1, 1)
        self.checkBoxXSS = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxXSS.setObjectName("checkBoxXSS")
        self.gridLayout_2.addWidget(self.checkBoxXSS, 2, 1, 1, 1)
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setStyleSheet("background-color: rgb(255, 183, 0);")
        self.testButton.setObjectName("testButton")
        self.gridLayout_2.addWidget(self.testButton, 4, 0, 1, 4)
        self.labelIP = QtWidgets.QLabel(self.centralwidget)
        self.labelIP.setObjectName("labelIP")
        self.gridLayout_2.addWidget(self.labelIP, 3, 3, 1, 1)
        self.ipInput = QtWidgets.QLineEdit(self.centralwidget)
        self.ipInput.setToolTip("")
        self.ipInput.setAccessibleName("")
        self.ipInput.setAccessibleDescription("")
        self.ipInput.setInputMask("")
        self.ipInput.setText("")
        self.ipInput.setObjectName("ipInput")
        self.gridLayout_2.addWidget(self.ipInput, 3, 4, 1, 1)
        self.checkBoxDDOS = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxDDOS.setObjectName("checkBoxDDOS")
        self.gridLayout_2.addWidget(self.checkBoxDDOS, 2, 0, 1, 1)
        self.labelPort = QtWidgets.QLabel(self.centralwidget)
        self.labelPort.setObjectName("labelPort")
        self.gridLayout_2.addWidget(self.labelPort, 3, 0, 1, 1)
        self.portInput = QtWidgets.QSpinBox(self.centralwidget)
        self.portInput.setMinimum(0)
        self.portInput.setMaximum(65535)
        self.portInput.setProperty("value", 80)
        self.portInput.setObjectName("portInput")
        self.gridLayout_2.addWidget(self.portInput, 3, 1, 1, 1)
        self.checkBoxSQLi = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxSQLi.setObjectName("checkBoxSQLi")
        self.gridLayout_2.addWidget(self.checkBoxSQLi, 2, 3, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 2, 4, 1, 1)
        self.checkBoxBF = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxBF.setObjectName("checkBoxBF")
        self.gridLayout_2.addWidget(self.checkBoxBF, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.cancelButton.setEnabled(False)
        self.cancelButton.clicked.connect(self.cancel)
        self.testButton.clicked.connect(self.startTest)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def startTest(self):
        try:
            print("checkbox :" + str(self.checkBoxBF.checkState()))
            ipaddress.IPv4Network(self.ipInput.text())
            # socket.inet_aton(self.ipInput.text())
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = WorkerTest(
                ip=self.ipInput.text(),
                port=self.portInput.text(),
                ddos=self.checkBoxDDOS.checkState(),
                xss=self.checkBoxXSS.checkState(),
                BF=self.checkBoxBF.checkState(),
                sqli=self.checkBoxSQLi.checkState())
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.addText.connect(self.addText)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.progressBar.setProperty("value", 0)
            self.progressBar.setMaximum(100)
            self.testButton.setEnabled(False)
            self.cancelButton.setEnabled(True)
            self.thread.finished.connect(
                lambda: self.testButton.setEnabled(True)
            )
            self.thread.finished.connect(
                lambda: self.progressBar.setProperty("value", 100))
            self.thread.finished.connect(
                lambda: self.cancelButton.setEnabled(False))
        except ValueError:
            self.addText("L'adresse IP entrée est au mauvais format ou est absente : " + self.ipInput.text(), "alert")
            self.addText("Veuillez saisir une adresse IP au format suivant : XXX.XXX.XXX.XXX ", "black")

    def addText(self, text, theme):
        self.displayOutput.append(self.textColor[theme] + text + self.textColor["end"])

    def cancel(self):
        self.worker.quit()
        print("Cancel")
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hacking"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.checkBoxXSS.setText(_translate("MainWindow", "XSS"))
        self.testButton.setText(_translate("MainWindow", "Test"))
        self.labelIP.setText(_translate("MainWindow", "IP address :"))
        self.ipInput.setPlaceholderText(_translate("MainWindow", "Ex. 192.145.21.1"))
        self.checkBoxDDOS.setText(_translate("MainWindow", "Dos/Ddos"))
        self.labelPort.setText(_translate("MainWindow", "Port : "))
        self.checkBoxSQLi.setText(_translate("MainWindow", "SQLi"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.checkBoxBF.setText(_translate("MainWindow", "Brut force"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
