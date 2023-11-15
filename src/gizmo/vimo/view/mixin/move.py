from PyQt5 import QtCore

class Move:

    canMove=True
    positionChanged=QtCore.pyqtSignal()

    def move(self, kind, digit=1):
        raise

    def movePage(self, kind, digit=1):
        raise
