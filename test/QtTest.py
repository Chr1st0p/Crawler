from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from mainwindow import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    form = App()
    form.show()
    application.exec_()
