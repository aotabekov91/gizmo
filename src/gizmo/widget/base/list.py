from PyQt5 import QtWidgets, QtCore, QtGui

class ListView(QtWidgets.QListView):

    indexChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, *args, **kwargs): 

        super().__init__(
                *args, **kwargs)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

    def move(self, kind, digit=1):

        def _move(arg):
            m=getattr(QtWidgets.QAbstractItemView, arg)
            i=self.moveCursor(m, QtCore.Qt.NoModifier)
            self.setCurrentIndex(i)

        func=None
        if kind=='up':
            func=lambda: _move('MoveUp')
        elif kind=='down':
            func=lambda: _move('MoveDown')
        if func:
            for i in range(digit): 
                func()

    def currentItem(self):

        m=self.model()
        if m:
            if hasattr(m, 'itemFromIndex'):
                return m.itemFromIndex(
                        self.currentIndex())
            elif type(m)==QtCore.QSortFilterProxyModel:
                index=m.mapToSource(
                        self.currentIndex())
                return m.itemFromIndex(index)

    def gotoFirst(self):
        self.goto(1)

    def gotoLast(self): 
        self.goto(self.model().rowCount())

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def goto(self, digit=1):

        idx=self.getRowIndex(digit-1)
        self.setCurrentIndex(idx)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        self.indexChanged.emit(idx)
