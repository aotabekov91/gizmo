from PyQt5 import QtCore, QtWidgets, QtGui

from gizmo.utils import MetaKey, register

class TreeWidget(QtWidgets.QTreeView, metaclass=MetaKey):

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

    @register('k')
    def up(self, digit=1):

        if self.currentIndex(): 
            for d in range(digit): 
                self.customMove('MoveUp')

    @register('j')
    def down(self, digit=1):

        if self.currentIndex(): 
            for d in range(digit): 
                self.customMove('MoveDown')

    @register('l')
    def expand(self, index=None):

        if index: 
            self.setCurrentIndex(index)
        super().expand(
                self.currentIndex())

    @register('e')
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

    @register('c')
    def collapseAll(self, index=None):

        if index is not None and index.isValid():
            if not self.isExpanded(index):
                self.collapse(index)
            for row in range(self.model().rowCount()):
                self.collapseAll(index.child(row,0))
        else:
            super().collapseAll()

    @register('H')
    def collapseAllInside(self, item=None):

        if item is None: 
            item=self.currentItem()
        if item:
            super().collapse(item.index())
            for i in range(item.rowCount()):
                self.collapseAllInside(
                        item.child(i))

    @register('h')
    def collapse(self, index=None):

        if index is None: 
            index=self.currentIndex()
        if index: 
            super().collapse(index)

    @register('d')
    def rootDown(self, digit=1):

        for d in range(digit):
            index=self.currentIndex()
            if index:
                self.setRootIndex(index)
                child=index.child(0,0)
                if child.isValid(): 
                    self.setCurrentIndex(child)

    @register('u')
    def rootUp(self, digit=1):

        for d in range(digit):
            index=self.rootIndex()
            if index.parent().isValid():
                self.setRootIndex(
                        index.parent())
                self.setCurrentIndex(
                        index)

    def customMove(self, direction):

        move=getattr(QtWidgets.QAbstractItemView, direction)
        index=self.moveCursor(
                move, 
                QtCore.Qt.NoModifier
                )
        self.setCurrentIndex(index)

    @register('gg')
    def gotoStart(self):

        index=self.rootIndex()
        if index: 
            child=index.child(0, 0)
            self.setCurrentIndex(child)

    @register('G')
    def gotoEnd(self): 

        index=self.rootIndex()
        if index: 
            last_row=self.model().rowCount(index)-1
            last=index.child(last_row, 0)
            self.setCurrentIndex(last)

    @register('gf')
    def gotoFirst(self): 

        index=self.currentIndex()
        if index:
            parent=index.parent()
            first=parent.child(0, 0)
            self.setCurrentIndex(first)

    @register('gl')
    def gotoLast(self): 

        index=self.currentIndex()
        if index:
            parent=index.parent()
            last_row=index.model().rowCount(parent)-1
            last=parent.child(last_row, 0)
            self.setCurrentIndex(last)

    @register('gp')
    def gotoParent(self):

        index=self.currentIndex()
        parent=index.parent()
        if parent.isValid(): self.setCurrentIndex(parent)

    @register('gs')
    def gotoSiblingDown(self, digit=1):

        for d in range(digit):
            self.gotoSibling(kind='down')

    @register('gS')
    def gotoSiblingUp(self, digit=1):

        for d in range(digit):
            self.gotoSibling(kind='up')

    def gotoSibling(self, kind='up'):

        idx=self.currentIndex()
        parent=idx.parent()
        if kind=='up':
            new=parent.child(
                    idx.row()-1, 0)
        else:
            new=parent.child(
                    idx.row()+1, 0)
        if new.isValid(): 
            self.setCurrentIndex(new)

    @register('G')
    def goto(self, digit=1):

        def getRowIndex(row):
            idx = self.model().index(0, 0)
            for i in range(row):
                idx = self.indexBelow(idx)
            return idx

        idx=getRowIndex(digit)
        self.setCurrentIndex(idx)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        if self.model() is None: 
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
            if item: self.itemChanged.emit(item)
        return super().event(event)

    # def keyPressEvent(self, event):
    #     self.keyPressEventOccurred.emit(event)
    #     if event.key()==QtCore.Qt.Key_J:
    #         self.moveDown()
    #     elif event.text()=='G':
    #         self.gotoEnd()
    #     elif event.key()==QtCore.Qt.Key_G:
    #         self.gotoStart()
    #     elif event.key()==QtCore.Qt.Key_BracketLeft:
    #         self.gotoSibling(kind='up')
    #     elif event.key()==QtCore.Qt.Key_BracketRight:
    #         self.gotoSibling(kind='down')
    #     elif event.key()==QtCore.Qt.Key_P:
    #         self.gotoParent()
    #     elif event.key()==QtCore.Qt.Key_K:
    #         self.moveUp()
    #     elif event.key()==QtCore.Qt.Key_L:
    #         self.expand()
    #     elif event.key()==QtCore.Qt.Key_H:
    #         self.collapse()
    #     elif event.key()==QtCore.Qt.Key_U:
    #         self.rootUp()
    #     elif event.key()==QtCore.Qt.Key_Z:
    #         self.update()
    #     elif event.key()==QtCore.Qt.Key_D:
    #         self.rootDown()
    #     elif event.key()==QtCore.Qt.Key_Semicolon:
    #         self.moveToParent()
    #     elif event.key()==QtCore.Qt.Key_B:
    #         self.moveToBottom()
    #     elif event.key()==QtCore.Qt.Key_X:
    #         self.expandAllInside()
    #     elif event.key()==QtCore.Qt.Key_T:
    #         self.collapseAllInside()
    #     elif event.key()==QtCore.Qt.Key_O:
    #         self.openWanted.emit()
    #     elif event.key()==QtCore.Qt.Key_Escape:
    #         self.hideWanted.emit()
    #     elif event.key()==QtCore.Qt.Key_Return:
    #         self.returnPressed.emit()
    #     else:
    #         super().keyPressEvent(event)
