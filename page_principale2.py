# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\imran\PycharmProjects\pythonProject\page_principale.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(554, 348)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_2.addWidget(self.checkBox_3, 2, 2, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 2, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_2.addWidget(self.checkBox_4, 2, 3, 1, 1)
        self.displayOutput = QtWidgets.QTextBrowser(self.centralwidget)
        self.displayOutput.setObjectName("displayOutput")
        self.gridLayout_2.addWidget(self.displayOutput, 0, 0, 1, 4)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 1, 0, 1, 4)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 4, 3, 1, 1)
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setStyleSheet("background-color: rgb(255, 183, 0);")
        self.testButton.setObjectName("testButton")
        self.gridLayout_2.addWidget(self.testButton, 4, 0, 1, 3)
        self.ipInput = QtWidgets.QLineEdit(self.centralwidget)
        self.ipInput.setToolTip("")
        self.ipInput.setAccessibleName("")
        self.ipInput.setAccessibleDescription("")
        self.ipInput.setInputMask("")
        self.ipInput.setText("")
        self.ipInput.setObjectName("ipInput")
        self.gridLayout_2.addWidget(self.ipInput, 3, 1, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hacking"))
        self.checkBox_3.setText(_translate("MainWindow", "SQLi"))
        self.checkBox_2.setText(_translate("MainWindow", "XSS"))
        self.checkBox.setText(_translate("MainWindow", "Dos/Ddos"))
        self.label.setText(_translate("MainWindow", "IP address :"))
        self.checkBox_4.setText(_translate("MainWindow", "Brut force"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.testButton.setText(_translate("MainWindow", "Test"))
        self.ipInput.setPlaceholderText(_translate("MainWindow", "Ex. 192.145.21.1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
