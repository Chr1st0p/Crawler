# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from draw.wordscloud import DrawStraitsTimesCloud
from parsers.KeywordParser import ParseKeywords
from utils.Paths import Paths


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(769, 745)
        MainWindow.setBaseSize(QtCore.QSize(20, 20))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Photo = QtWidgets.QLabel(self.centralwidget)
        self.Photo.setGeometry(QtCore.QRect(10, 70, 751, 651))
        self.Photo.setText("")
        self.Photo.setObjectName("Photo")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 20, 751, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.YearLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(20)
        self.YearLabel.setFont(font)
        self.YearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.YearLabel.setObjectName("YearLabel")
        self.horizontalLayout.addWidget(self.YearLabel)
        self.YearSpin = QtWidgets.QSpinBox(self.widget)
        self.YearSpin.setSizeIncrement(QtCore.QSize(20, 20))
        self.YearSpin.setBaseSize(QtCore.QSize(20, 20))
        self.YearSpin.setMinimum(2016)
        self.YearSpin.setMaximum(2017)
        self.YearSpin.setObjectName("YearSpin")
        self.horizontalLayout.addWidget(self.YearSpin)
        self.MonthLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(20)
        self.MonthLabel.setFont(font)
        self.MonthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MonthLabel.setObjectName("MonthLabel")
        self.horizontalLayout.addWidget(self.MonthLabel)
        self.MonthSpin = QtWidgets.QSpinBox(self.widget)
        self.MonthSpin.setMinimum(1)
        self.MonthSpin.setMaximum(12)
        self.MonthSpin.setObjectName("MonthSpin")
        self.horizontalLayout.addWidget(self.MonthSpin)
        self.GenerateBTN = QtWidgets.QPushButton(self.widget)
        self.GenerateBTN.clicked.connect(self.wrapper)
        self.horizontalLayout.addWidget(self.GenerateBTN)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.YearLabel.setText(_translate("MainWindow", "Year"))
        self.MonthLabel.setText(_translate("MainWindow", "Month"))
        self.GenerateBTN.setText(_translate("MainWindow", "Generate"))

    def wrapper(self):
        ParseKeywords(self.YearSpin.value(), self.MonthSpin.value())
        DrawStraitsTimesCloud(self.YearSpin.value(), self.MonthSpin.value())
        self.Photo.setPixmap(
            QtGui.QPixmap(Paths.imagespath + str(self.YearSpin.value()) + str(self.MonthSpin.value()) + ".png"))
