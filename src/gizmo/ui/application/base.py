from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtWidgets import QApplication

class Application(QtWidgets.QApplication):

    earSet=QtCore.pyqtSignal(object)
    earGained=QtCore.pyqtSignal(object)
