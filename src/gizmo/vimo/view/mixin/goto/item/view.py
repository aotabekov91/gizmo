from PyQt5 import QtCore, QtWidgets

from ..base import Go

class ViewGo(Go):

    def goTo(self, digit=None):

        if digit is None:
            self.goToLast()
        else:
            idx=self.getRowIndex(digit-1)
            self.setCurrentIndex(idx)

    def goToFirst(self):
        self.goTo(1)

    def goToLast(self): 

        c=self.model().rowCount()
        self.goTo(c)

    def goToUp(self, digit=1):

        for i in range(digit): 
            self.move('MoveUp')

    def goToDown(self, digit=1):

        for i in range(digit): 
            self.move('MoveDown')

    def move(self, arg):

        m=getattr(QtWidgets.QAbstractItemView, arg, None)
        if not m is None:
            i=self.moveCursor(m, QtCore.Qt.NoModifier)
            self.setCurrentIndex(i)

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        if type(idx)==int:
            self.indexChanged.emit(idx)
        else:
            self.indexChanged.emit(idx.row()+1)
