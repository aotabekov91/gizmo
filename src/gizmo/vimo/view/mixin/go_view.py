from PyQt5 import QtCore

from .go import Go

class ViewGo(Go):

    indexChanged=QtCore.pyqtSignal(object)

    def goto(self, digit=1):

        idx=self.getRowIndex(digit-1)
        self.setCurrentIndex(idx)

    def go(self, kind, *args, **kwargs):

        if type(kind)==int:
            self.goto(kind)
        elif kind=='first':
            if hasattr(self, 'gotoFirst'):
                self.gotoFirst()
        elif kind=='last':
            if hasattr(self, 'gotoLast'):
                self.gotoLast()

    def count(self):
        return self.model().rowCount()

    def gotoFirst(self):
        self.goto(1)

    def gotoLast(self): 
        self.goto(self.count())

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        self.indexChanged.emit(idx.row()+1)
