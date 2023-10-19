from PyQt5 import QtWidgets, QtCore, QtGui

class Application(QtWidgets.QApplication):

    earSet=QtCore.pyqtSignal(object)
    earGained=QtCore.pyqtSignal(object)
