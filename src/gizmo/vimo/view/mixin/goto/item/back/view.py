from PyQt5 import QtCore

from .base import Go

class ViewGo(Go):

    indexChanged=QtCore.pyqtSignal(object)

    def goTo(self, digit=1):

        idx=self.getRowIndex(digit-1)
        self.setCurrentIndex(idx)

    def goToFirst(self):
        self.goTo(1)

    def goToLast(self): 

        c=self.model().rowCount()
        self.goTo(c)

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        self.indexChanged.emit(idx.row()+1)
