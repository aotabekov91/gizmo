from PyQt5 import QtWidgets, QtCore

class Go:

    canGo=True
    indexChanged=QtCore.pyqtSignal(object)

    def go(self, kind, *args, **kwargs):

        k=kind.title()
        f=getattr(self, 'goto{k}', None)
        if f: f(*args, **kwargs)

        if type(kind)==int:
            self.goTo(kind)
        elif kind=='first':
            if hasattr(self, 'gotoFirst'):
                self.goToFirst()
        elif kind=='last':
            if hasattr(self, 'gotoLast'):
                self.goToLast()

    def goTo(self, digit=1):

        idx=self.getRowIndex(digit-1)
        self.setCurrentIndex(idx)


    def goToLast(self): 

        c=self.model().rowCount()
        self.goTo(c)

    def goToUp(self, digit=1):

        for i in range(digit): 
            self.move('MoveUp')

    def goToDown(self, digit=1):

        for i in range(digit): 
            self.move('MoveDown')

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        self.indexChanged.emit(idx.row()+1)

    def move(self, arg):

        m=getattr(QtWidgets.QAbstractItemView, arg, None)
        if not m is None:
            i=self.moveCursor(m, QtCore.Qt.NoModifier)
            self.setCurrentIndex(i)
