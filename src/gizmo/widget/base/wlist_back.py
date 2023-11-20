from PyQt5 import QtCore, QtWidgets

class ListWidget(QtWidgets.QListWidget):

    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            parent=None,
            item_widget=None, 
            ignore_case=True, 
            exact_match=False, 
            enable_filter=True, 
            objectName='ListWidget', 
            field_rematch=lambda x: x, 
            check_fields=['up', 'down'], 
            text_non_found='No match found', 
            item_position='PositionAtCenter', 
            **kwargs
            ):

        super().__init__(
                parent=parent,
                objectName=objectName)
        self.dlist = []
        self.flist = []
        self.item_widget=item_widget
        self.exact_match=exact_match
        self.ignore_case=ignore_case
        self.check_fields=check_fields
        self.field_rematch=field_rematch
        self.enable_filter=enable_filter
        self.item_position=item_position
        self.text_non_found=text_non_found
        self.setUI()

    def setUI(self):

        self.setSpacing(2)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)

    def addItem(self, d):

        if self.item_widget:
            w = self.item_widget(self, d) 
            super().addItem(w.listItem())
            super().setItemWidget(w.listItem(), w)

    def widget(self): 
        return self.item_widget(self)

    def move(self, kind, digit=1):

        r = self.currentRow()
        if r==None: 
            return
        if kind=='down':
            r+=digit
        elif kind=='up':
            r-=digit
        else:
            raise
        if r < 0:
            r = self.count()-1
        elif r >= self.count():
            r = 0
        self.setCurrentRow(r)
        h=getattr(
                QtWidgets.QAbstractItemView, 
                self.item_position,
                'PositionAtCenter')
        i=self.currentItem()
        self.itemChanged.emit(i)
        self.scrollToItem(i, hint=h)

    def sizeHint(self):

        hint=super().sizeHint()
        height=5
        if self.count()>0:
            for i in range(self.count()):
                height += self.item(i).sizeHint().height()
        hint.setHeight(height)
        return hint

    def setItem(self, condDict):

        for i in range(self.count()):
            item=self.item(i)
            data=item.itemData
            found=item
            for k, v in condDict.items():
                if data.get(k, None)!=v: 
                    return False
            self.setCurrentItem(found)

    def setList(self, dlist):

        dlist = dlist or []
        self.dlist=self.flist=dlist
        self.addItems(dlist)

    def refresh(self, clear=False):

        tlist=self.filterList()
        if clear: 
            tlist=self.dataList()
        r=self.currentRow()
        self.addItems(tlist)
        self.setCurrentRow(r)

    def setEnableFilter(self, condition): 
        self.enable_filter=condition

    def unfilter(self): 

        if self.flist!=self.dlist: 
            self.setList(self.dlist)

    def filter(self, text):

        if self.enable_filter:
            super().clear()
            if len(self.dlist)==0: 
                dlist=[{'up': text}] 
            else:
                if not text:
                    dlist=self.dlist
                else:
                    dlist=[]
                    for data in self.dlist:
                        if self.isin(text, data): 
                            dlist+=[data]
            self.setFilterList(dlist)
            self.setCurrentRow(0)

    def setFilterList(self, dlist):

        self.flist=dlist
        self.addItems(dlist)

    def isin(self, text, data):

        for f in self.check_fields:
            ft= str(data.get(f, ''))
            if self.exact_match:
                if ft and text==ft[:len(text)]: 
                    return True
            else:
                if self.ignore_case:
                    if ft and text.lower() in ft.lower(): 
                        return True
                else:
                    if ft and text in ft: 
                        return True
        return False

    def dataList(self): 
        return self.dlist

    def filterList(self): 
        return self.flist

    def addItems(self, dlist): 

        self.clear()
        dlist=dlist or []
        for d in dlist:
            self.addItem(d)
        self.setCurrentRow(0)
        self.adjustSize()

    def focusItem(self, row=None):

        if not row: 
            row=self.currentRow()
            item=self.currentItem()
        else:
            for i in range(self.count()):
                if i==row:
                    item=self.item(i)
                    break
        if item: 
            self.setCurrentRow(row)
            self.itemWidget(item).setFocus()

    def getWidget(self, row=None): 

        row = row or self.currentRow()
        for i in range(self.count()):
            if i==row: 
                return self.itemWidget(self.item(i))

    def adjustSize(self, width=None, height=None):

        if not width or not height: 

            if self.parent(): 
                width=self.parent().size().width()
                height=self.parent().size().height()
            else:
                width=self.size().width()
                height=self.size().height()

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        for i in range(self.count()): 
            self.item(i).widget.setFixedWidth(width)
        super().adjustSize()
