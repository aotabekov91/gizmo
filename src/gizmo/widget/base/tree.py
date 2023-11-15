from gizmo.utils import tag
from PyQt5 import QtCore, QtWidgets, QtGui

class TreeWidget(QtWidgets.QTreeView):

    openWanted=QtCore.pyqtSignal()
    hideWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    keysChanged=QtCore.pyqtSignal(str)
    itemChanged=QtCore.pyqtSignal(object)
    indexChanged=QtCore.pyqtSignal(object)
    keyPressed=QtCore.pyqtSignal(object, object)
    keyPressEventOccurred=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            *args, 
            **kwargs
            ): 

        super().__init__(
                *args, 
                **kwargs
                )
        self.setHeaderHidden(True)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

    def currentItem(self):

        m=self.model()
        if m:
            if type(m)==QtGui.QStandardItemModel:
                return m.itemFromIndex(
                        self.currentIndex())
            elif hasattr(m, 'itemFromIndex'):
                return m.itemFromIndex(
                        self.currentIndex())
            elif type(m)==QtCore.QSortFilterProxyModel:
                index=m.mapToSource(
                        self.currentIndex())
                return m.itemFromIndex(index)

    @tag('k')
    def up(self, digit=1):

        if self.currentIndex(): 
            for d in range(digit): 
                self.customMove('MoveUp')

    @tag('j')
    def down(self, digit=1):

        if self.currentIndex(): 
            for d in range(digit): 
                self.customMove('MoveDown')

    @tag('l')
    def expand(self, index=None):

        if index: 
            self.setCurrentIndex(index)
        super().expand(
                self.currentIndex())

    @tag('e')
    def expandAll(self, index=None):

        if index is None:
            super().expandAll()
        elif index.isValid():
            if not self.isExpanded(index): 
                self.expand(index)
            for row in range(self.model().rowCount()):
                self.expandAll(index.child(row,0))

    def expandAbove(self, child):

        index=child.parent()
        while index.isValid():
            index=index.parent()
            self.expand(index)

    @tag('c')
    def collapseAll(self, index=None):

        if index is not None and index.isValid():
            if not self.isExpanded(index):
                self.collapse(index)
            for row in range(self.model().rowCount()):
                self.collapseAll(index.child(row,0))
        else:
            super().collapseAll()

    @tag('H')
    def collapseAllInside(self, item=None):

        if item is None: 
            item=self.currentItem()
        if item:
            super().collapse(item.index())
            for i in range(item.rowCount()):
                self.collapseAllInside(
                        item.child(i))

    @tag('h')
    def collapse(self, index=None):

        if index is None: 
            index=self.currentIndex()
        if index: 
            super().collapse(index)

    @tag('d')
    def rootDown(self, digit=1):

        for d in range(digit):
            index=self.currentIndex()
            if index:
                self.setRootIndex(index)
                child=index.child(0,0)
                self.setCurrentIndex(child)

    @tag('u')
    def rootUp(self, digit=1):

        for d in range(digit):
            idx=self.rootIndex()
            p=idx.parent()
            if p.isValid():
                self.setRootIndex(p)
                self.setCurrentIndex(idx)

    def customMove(self, direction):

        move=getattr(QtWidgets.QAbstractItemView, direction)
        index=self.moveCursor(
                move, 
                QtCore.Qt.NoModifier
                )
        self.setCurrentIndex(index)

    @tag('gg')
    def gotoFirst(self):

        index=self.rootIndex()
        if index: 
            child=index.child(0, 0)
            self.setCurrentIndex(child)

    @tag('gf')
    def gotoFirstSibling(self): 

        idx=self.currentIndex()
        if idx:
            p=idx.parent()
            f=p.child(0, 0)
            self.setCurrentIndex(f)

    def gotoLast(self): 

        index=self.rootIndex()
        if index: 
            last_row=self.model().rowCount(index)-1
            last=index.child(last_row, 0)
            self.setCurrentIndex(last)

    @tag('gl')
    def gotoLastSibling(self): 

        index=self.currentIndex()
        if index:
            parent=index.parent()
            last_row=index.model().rowCount(parent)-1
            last=parent.child(last_row, 0)
            self.setCurrentIndex(last)

    @tag('G')
    def goto(self, digit=None):

        if digit is None:
            self.gotoLast()
        else:
            idx=self.getRowIndex(digit)
            self.setCurrentIndex(idx)

    def getRowIndex(self, row):

        idx = self.model().index(0, 0)
        for i in range(row):
            idx = self.indexBelow(idx)
        return idx

    @tag('gp')
    def gotoParent(self):

        index=self.currentIndex()
        parent=index.parent()
        self.setCurrentIndex(parent)

    @tag('gs')
    def gotoSiblingDown(self, digit=1):

        for d in range(digit):
            self.gotoSibling(kind='down')

    @tag('gS')
    def gotoSiblingUp(self, digit=1):

        for d in range(digit):
            self.gotoSibling(kind='up')

    def gotoSibling(self, kind='up'):

        idx=self.currentIndex()
        p=idx.parent()
        s_idx=idx.row()+1
        if kind=='up': 
            s_idx=idx.row()-1
        n_idx=p.child(s_idx, 0)
        self.setCurrentIndex(n_idx)

    def setCurrentIndex(self, idx):

        if self.model() is None: 
            return
        if idx is None:
            return
        super().setCurrentIndex(idx)
        if not idx.isValid():
            return
        if self.currentItem() is None: 
            return
        self.indexChanged.emit(
                idx)
        self.itemChanged.emit(
                self.currentItem())
        self.selectionModel().select(
                idx, 
                QtCore.QItemSelectionModel.Current)
        if hasattr(self.model(), 'itemChanged'):
            self.model().itemChanged.emit(
                    self.currentItem())

    def event(self, event):

        if event.type()==QtCore.QEvent.Enter:
            item=self.currentItem()
            if item: 
                self.itemChanged.emit(item)
        return super().event(event)
