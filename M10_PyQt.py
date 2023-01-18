import sys

import M5_Network
import pygame

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLCDNumber, QFileDialog, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap, QImage, QColor, QTransform
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Connection_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(395, 102)
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(120, 10, 271, 20))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 30, 211, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(120, 70, 131, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Подключение"))
        self.label.setText(_translate("widget", "Введите IP-адрес сервера"))
        self.pushButton.setText(_translate("widget", "Подключиться"))

class Connection(QDialog, Ui_Connection_widget):
    def __init__(self, perent):
        super().__init__()
        self.setupUi(self)
        self.perent = perent
        self.pushButton.clicked.connect(self.accept)

class Ui_Start_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(390, 102)
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 371, 81))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Стартовое окно"))
        self.pushButton.setText(_translate("widget", "Подключиться"))

class Start(QMainWindow, Ui_Start_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.p1_n)

    def p1_n(self):
        self.ok_pressed = Connection(self)
        p = self.ok_pressed.exec_()
        if p:
            self.hide()
            import M9_Cycles
            print(self.ok_pressed.lineEdit.text())
            try:
                M9_Cycles.Game_body(M5_Network.Network(self.ok_pressed.lineEdit.text()))
            except Exception as a:
                self.show()
                print(a)
                pygame.quit()