from PyQt5 import QtCore, QtGui, QtWidgets

class TreeView(QtWidgets.QTreeView):

    itemChanged=QtCore.pyqtSignal(object)
    indexChanged=QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs): 

        super().__init__(
                *args, **kwargs)
        self.setHeaderHidden(True)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

    def currentItem(self, idx=None):

        m=self.model()
        if m:
            idx = idx or self.currentIndex()
            if type(m)==QtCore.QSortFilterProxyModel:
                idx=m.mapToSource(idx)
            if idx and hasattr(m, 'itemFromIndex'):
                return m.itemFromIndex(idx)

    def expand(self, idx=None):

        idx = idx or self.currentIndex()
        self.setCurrentIndex(idx)
        super().expand(idx)

    def expandAll(self, idx=None):

        if idx is None:
            super().expandAll()
        elif idx.isValid():
            if not self.isExpanded(idx): 
                self.expand(idx)
            for row in range(self.model().rowCount()):
                self.expandAll(idx.child(row,0))

    def expandAbove(self, child):

        index=child.parent()
        while index.isValid():
            index=index.parent()
            self.expand(index)

    def collapseAll(self, idx=None):

        if idx is not None and idx.isValid():
            if not self.isExpanded(idx):
                self.collapse(idx)
            for row in range(self.model().rowCount()):
                self.collapseAll(idx.child(row,0))
        else:
            super().collapseAll()

    def collapseAllInside(self, item=None):

        item = item or self.currentItem()
        if item:
            super().collapse(item.index())
            for i in range(item.rowCount()):
                self.collapseAllInside(
                        item.child(i))

    def collapse(self, idx=None):

        idx = idx or self.currentIndex()
        super().collapse(idx)

    def rootDown(self, digit=1):

        for d in range(digit):
            idx=self.currentIndex()
            if idx:
                self.setRootIndex(idx)
                child=idx.child(0,0)
                self.setCurrentIndex(child)

    def rootUp(self, digit=1):

        for d in range(digit):
            idx=self.rootIndex()
            p=idx.parent()
            if p.isValid():
                self.setRootIndex(p)
                self.setCurrentIndex(idx)

    def move(self, kind, digit=1):

        def _move(arg):
            m=getattr(QtWidgets.QAbstractItemView, arg)
            i=self.moveCursor(m, QtCore.Qt.NoModifier)
            self.setCurrentIndex(i)

        if kind=='up':
            func=lambda: _move('MoveUp')
        elif kind=='down':
            func=lambda: _move('MoveDown')
        elif kind=='left':
            func=self.collapse
        elif kind=='right':
            func=self.expand
        for i in range(digit): func()

    def goToFirst(self):

        idx=self.rootIndex()
        if idx: 
            child=idx.child(0, 0)
            self.setCurrentIndex(child)
            
    def goToLast(self): 

        idx=self.rootIndex()
        if idx: 
            m=self.model()
            lr=m.rowCount(idx)-1
            last=idx.child(lr, 0)
            self.setCurrentIndex(last)

    def goToFirstSibling(self): 

        idx=self.currentIndex()
        if idx:
            p=idx.parent()
            f=p.child(0, 0)
            self.setCurrentIndex(f)

    def goToLastSibling(self): 

        index=self.currentIndex()
        if index:
            parent=index.parent()
            last_row=index.model().rowCount(parent)-1
            last=parent.child(last_row, 0)
            self.setCurrentIndex(last)

    def goTo(self, digit=1):

        idx=self.getRowIndex(digit)
        self.setCurrentIndex(idx)

    def getRowIndex(self, row):

        idx = self.model().index(0, 0)
        for i in range(row):
            idx = self.indexBelow(idx)
        return idx

    def goToParent(self):

        idx=self.currentIndex()
        self.setCurrentIndex(idx.parent())

    def goToSiblingDown(self, digit=1):

        for d in range(digit):
            self.goToSibling(kind='down')

    def goToSiblingUp(self, digit=1):

        for d in range(digit):
            self.goToSibling(kind='up')

    def goToSibling(self, kind='up'):

        idx=self.currentIndex()
        p=idx.parent()
        s_idx=idx.row()+1
        if kind=='up': 
            s_idx=idx.row()-1
        n_idx=p.child(s_idx, 0)
        self.setCurrentIndex(n_idx)

    def setCurrentIndex(self, idx):

        if idx is None: return
        if not idx.isValid(): return
        if self.model() is None: return
        super().setCurrentIndex(idx)
        if self.currentItem() is None: return
        self.indexChanged.emit(idx)
        self.itemChanged.emit(
                self.currentItem())
        self.selectionModel().select(
                idx, 
                QtCore.QItemSelectionModel.Current)
        if hasattr(self.model(), 'itemChanged'):
            self.model().itemChanged.emit(
                    self.currentItem())
