from PyQt5 import QtCore, QtWidgets, QtGui

from gizmo.utils import SetKeys, register

class TreeWidget(QtWidgets.QTreeView, metaclass=SetKeys):

    openWanted=QtCore.pyqtSignal()
    hideWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    keyPressed=QtCore.pyqtSignal(object, object)

    itemChanged=QtCore.pyqtSignal(object)
    indexChanged=QtCore.pyqtSignal(object)
    keyPressEventOccurred=QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs): 

        super().__init__(*args, **kwargs)

        self.setHeaderHidden(True)

        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

        self.setUI()

    def setUI(self):

        self.style_sheet = '''
            QTreeView{
                border-width: 0px;
                color: transparent;
                border-color: transparent; 
                background-color: transparent; 
                show-decoration-selected: 0;
                }

            QTreeView::item{
                color: white;
                border-color: transparent;
                background-color: transparent;
                border-radius: 0px;
                padding: 5px 5px 5px 10px;
                }
            QTreeView::item:selected{
                color: black;
                background-color: yellow;
                }
                '''

        self.setStyleSheet(self.style_sheet)

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
                index=m.mapToSource(self.currentIndex())
                return m.itemFromIndex(index)

    @register('k')
    def moveUp(self):

        if self.currentIndex(): 
            self.customMove('MoveUp')

    @register('j')
    def moveDown(self):

        if self.currentIndex(): 
            self.customMove('MoveDown')

    @register('l')
    def expand(self, index=None):

        if index: self.setCurrentIndex(index)
        super().expand(self.currentIndex())

    def expandAllInside(self, item=None):

        if item is None: item=self.currentItem()
        if item is None: return
        super().expand(item.index())
        for i in range(item.rowCount()):
            self.expandAllInside(item.child(i))

    def expandAll(self, index=None):

        if index is None:
            super().expandAll()
        elif index.isValid():
            if not self.isExpanded(index): self.expand(index)
            for row in range(self.model().rowCount()):
                self.expandAll(index.child(row,0))

    def expandAbove(self, child):

        index=child.parent()
        while index.isValid():
            index=index.parent()
            self.expand(index)

    def collapseAll(self, index=None):

        if index is not None and index.isValid():
            if not self.isExpanded(index):
                self.collapse(index)
            for row in range(self.model().rowCount()):
                self.collapseAll(index.child(row,0))
        else:
            super().collapseAll()

    def collapseAllInside(self, item=None):

        if item is None: item=self.currentItem()
        if item is None: return
        super().collapse(item.index())
        for i in range(item.rowCount()):
            self.collapseAllInside(item.child(i))

    @register('h')
    def collapse(self, index=None):

        if index is None: index=self.currentIndex()
        if index: super().collapse(index)

    def rootDown(self):

        index=self.currentIndex()
        if index:
            self.setRootIndex(index)
            child=index.child(0,0)
            if child.isValid(): self.setCurrentIndex(child)

    def rootUp(self):

        index=self.rootIndex()
        if index.parent().isValid():
            self.setRootIndex(index.parent())
            self.setCurrentIndex(index)

    def customMove(self, direction):

        action=getattr(QtWidgets.QAbstractItemView, direction)
        ind=self.moveCursor(action, QtCore.Qt.NoModifier)
        self.setCurrentIndex(ind)

    @register('gg')
    def gotoStart(self):

        index=self.rootIndex()
        if index: self.setCurrentIndex(index.child(0, 0))

    def gotoParent(self):

        index=self.currentIndex()
        parent=index.parent()
        if parent.isValid(): self.setCurrentIndex(parent)

    @register('Ctrl+w Shift+s')
    def gotoSibling(self, kind='up'):

        index=self.currentIndex()
        parent=index.parent()

        if kind=='up':
            new=parent.child(index.row()-1, 0)
        else:
            new=parent.child(index.row()+1, 0)
        if new.isValid(): 
            self.setCurrentIndex(new )

    @register('Shift+e Ctrl+a')
    def gotoEnd(self): 

        index=self.currentIndex()
        if index:
            parent=index.parent()
            last=parent.child(
                    index.model().rowCount(parent)-1, 0)
            self.setCurrentIndex(last)

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

    def setCurrentIndex(self, index):

        super().setCurrentIndex(index)
        if self.model() is None: return
        if self.currentItem() is None: return
        self.indexChanged.emit(index)
        self.itemChanged.emit(self.currentItem())

    def event(self, event):

        if event.type()==QtCore.QEvent.Enter:
            item=self.currentItem()
            if item: self.itemChanged.emit(item)
        return super().event(event)
