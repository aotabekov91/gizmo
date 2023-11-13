from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtWidgets import QApplication

class Application(QtWidgets.QApplication):

    earSet=QtCore.pyqtSignal(object)
    earGained=QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):

        self.ears=[]
        super().__init__(*args, **kwargs)
        self.earSet.connect(self.addEar)
        self.earGained.connect(self.setEar)

    def addEar(self, ear):
        self.ears+=[ear]

    def setEar(self, ear):
        self.current=ear
