import re
from PyQt5 import QtCore, QtWidgets
from gizmo.utils import MetaKey, register

from ..items import IconUpDown

class WidgetList(QtWidgets.QListWidget, metaclass=MetaKey):

    hideWanted=QtCore.pyqtSignal()
    openWanted=QtCore.pyqtSignal(
            object)
    returnPressed=QtCore.pyqtSignal()
    widgetDataChanged=QtCore.pyqtSignal(
            object)

    def __init__(
            self, 
            objectName='List', 
            widget=IconUpDown, 
            hint=QtWidgets.QAbstractItemView.PositionAtCenter,
            **kwargs
            ):

        self.dlist = []
        self.flist = []
        self.hint = hint
        self.widget=widget
        super().__init__(
                objectName=objectName)
        self.setUI()

    def setUI(self):

        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)

    def move(self, digit):

        rnum = self.currentRow()
        if rnum is not None:
            c=self.count()
            rnum += digit
            if rnum<0: rnum=c-1
            if rnum>c-1: rnum=0
            self.setCurrentRow(rnum)
            self.scrollToItem(
                    self.currentItem(), 
                    hint=self.hint)
            self.itemChanged.emit(
                    self.currentItem())

    def sizeHint(self):

        h=5
        for i in range(self.count()):
            ih = self.item(i).sizeHint()
            h += ih.height()
        hint=super().sizeHint()
        hint.setHeight(h)
        return hint

    def setList(
            self, 
            dlist=[], 
            flist=None,
            ):

        self.dlist=dlist
        if not flist:
            flist=dlist
        self.flist=flist
        self.addItems(flist)
        self.setCurrentRow(0)

    def refresh(self, clear=False):

        tmp=self.flist
        if clear: 
            tmp=self.dlist
        nrow=self.currentRow()
        self.addItems(tmp)
        self.setCurrentRow(nrow)

    def filter(
            self, 
            flags=0,
            fields={},
            ):

        flist=[]
        for d in self.dlist:
            match=True
            for n, r in fields.items(): 
                t = str(d.get(n, ''))
                r=re.compile(r, flags) 
                if not re.match(r, t):
                    match=False
                    break
            if match: 
                flist+=[d]
        self.flist=flist
        self.addItems(flist)
        self.setCurrentRow(0)

    def removeItems(self):

        for i in range(self.count()):
            self.takeItem(i)

    def addItems(self, dlist=[]): 

        self.clear()
        for i, d in enumerate(dlist):
            w = self.widget(self, d) 
            super().addItem(w.item)
            super().setItemWidget(
                    w.item, w)
        # self.adjustSize()

    @register(['j', 'n'])
    def moveDown(self, digit=1): 
        self.move(digit)

    @register(['k', 'p'])
    def moveUp(self, digit=1): 

        if digit>0: 
            digit=-1*digit
        self.move(digit)

    @register('l')
    def setFocusItem(self):

        i=self.currentItem()
        if i: 
            w=self.itemWidget(i)
            w.setFocus()

    @register('<c-h>')
    def setFocus(self):
        super().setFocus()
