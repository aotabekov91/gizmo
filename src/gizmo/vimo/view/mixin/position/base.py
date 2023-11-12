from PyQt5 import QtCore

class Position:

    canPosition=True
    positionChanged=QtCore.pyqtSignal()

    def getPosition(self, *args, **kwargs): 
        pass

    def goto(self, *args, **kwarrgs):
        pass

    def gotoFirst(self, *args, **kwargs):
        pass

    def gotoLast(self, *args, **kwargs):
        pass
