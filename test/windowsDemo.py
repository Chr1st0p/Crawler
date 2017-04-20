# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowDemo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.photo = QtWidgets.QLabel(Dialog)
        self.photo.setGeometry(QtCore.QRect(50, 60, 301, 211))
        self.photo.setText("")
        self.photo.setObjectName("photo")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(50, 20, 303, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.YearLabel = QtWidgets.QLabel(self.widget)
        self.YearLabel.setObjectName("YearLabel")
        self.horizontalLayout.addWidget(self.YearLabel)
        self.YearBox = QtWidgets.QSpinBox(self.widget)
        self.YearBox.setMinimum(2016)
        self.YearBox.setMaximum(2017)
        self.YearBox.setObjectName("YearBox")
        self.horizontalLayout.addWidget(self.YearBox)
        self.MonthLabel = QtWidgets.QLabel(self.widget)
        self.MonthLabel.setObjectName("MonthLabel")
        self.horizontalLayout.addWidget(self.MonthLabel)
        self.MonthBox = QtWidgets.QSpinBox(self.widget)
        self.MonthBox.setMinimum(1)
        self.MonthBox.setMaximum(12)
        self.MonthBox.setObjectName("MonthBox")
        self.horizontalLayout.addWidget(self.MonthBox)
        self.GenerateButton = QtWidgets.QPushButton(self.widget)
        self.GenerateButton.setObjectName("GenerateButton")
        self.horizontalLayout.addWidget(self.GenerateButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.YearLabel.setText(_translate("Dialog", "Year"))
        self.MonthLabel.setText(_translate("Dialog", "Month"))
        self.GenerateButton.setText(_translate("Dialog", "Ok"))
