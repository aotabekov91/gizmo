from PyQt5 import QtCore, QtWidgets
from gizmo.utils import MetaKey, register

from .items import IconUpDown

class ListWidget(QtWidgets.QListWidget, metaclass=MetaKey):

    hideWanted=QtCore.pyqtSignal()
    openWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(self, 
                 item_widget=IconUpDown, 
                 check_fields=['up', 'down'],
                 ignore_case=True,
                 exact_match=False,
                 enable_filter=True,
                 field_rematch=lambda x: x,
                 text_non_found='No match found',
                 set_base_style=True,
                 item_position='PositionAtCenter',
                 objectName='List',
                 **kwargs):

        super(ListWidget, self).__init__(
                objectName=objectName,
                **kwargs)
        self.dlist = []
        self.flist = []
        self.listener=None
        self.item_widget=item_widget
        self.exact_match=exact_match
        self.ignore_case=ignore_case
        self.check_fields=check_fields
        self.field_rematch=field_rematch
        self.enable_filter=enable_filter
        self.item_position=item_position
        self.text_non_found=text_non_found
        self.set_base_style=set_base_style
        self.setUI()

    def setBaseStyleSheet(self):

        style_sheet = '''
            QListWidget{
                border-width: 0px;
                color: transparent;
                border-color: transparent; 
                background-color: transparent; 
                }
            QListWidget::item{
                border-radius: 10px;
                border-style: outset;
                padding: 0px 0px 0px 0px;
                color: transparent;
                background-color: #101010;
                }
            QListWidget::item:selected {
                border-width: 3px;
                border-color: red;
                }
                '''
        # self.setStyleSheet(style_sheet)

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
        if self.set_base_style:
            self.setBaseStyleSheet()

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.listener=listener
        for i in range(self.count()):
            item=self.item(i)
            item.widget.installEventFilter(self.listener)

    def addItem(self, data):

        widget = self.item_widget(
                self, 
                data, 
                set_base_style=self.set_base_style)
        if self.listener: 
            widget.installEventFilter(self.listener)
        super().addItem(widget.listItem())
        super().setItemWidget(widget.listItem(), widget)

    def widget(self): 

        return self.item_widget(self)

    def move(self, crement=-1):

        # self.setFocus()
        crow = self.currentRow()
        if crow==None: return
        crow += crement
        if crow < 0:
            crow = self.count()-1
        elif crow >= self.count():
            crow = 0
        self.setCurrentRow(crow)
        hint=getattr(QtWidgets.QAbstractItemView,
                     self.item_position,
                     'PositionAtCenter')
        self.scrollToItem(
                self.currentItem(), hint=hint)
        self.itemChanged.emit(self.currentItem())

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

    def setList(self, dlist, limit=30):

        if dlist is None: 
            dlist=[]
        self.dlist=dlist
        self.flist=dlist
        self.addItems(dlist, limit=limit)

    def refresh(self, clear=False):

        tempList=self.filterList()
        if clear: tempList=self.dataList()
        crow=self.currentRow()
        self.addItems(tempList)
        self.setCurrentRow(crow)

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
                        if self.isin(text, data): dlist+=[data]

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

    def dataList(self): return self.dlist

    def filterList(self): return self.flist

    def addItems(self, dlist, limit=30): 

        self.clear()
        if dlist:
            for i, data in enumerate(dlist):
                if limit and i>limit: break
                self.addItem(data)
            self.setCurrentRow(0)
        self.setCurrentRow(0)
        self.adjustSize()

    @register('j')
    def moveDown(self): 

        self.move(crement=1)

    @register('k')
    def moveUp(self): 

        self.move(crement=-1)

    @register('<c-[>')
    def wantHide(self): 

        self.hideWanted.emit()

    @register('<c-m>')
    def pressReturn(self): 

        self.returnPressed.emit()

    def keyPressEvent(self, event):

        if event.key() in [QtCore.Qt.Key_J, 
                           QtCore.Qt.Key_N]:
            self.move(crement=1)
        elif event.key() in [QtCore.Qt.Key_K, 
                             QtCore.Qt.Key_P]:
            self.move(crement=-1)
        elif event.key() in  [QtCore.Qt.Key_M, 
                              QtCore.Qt.Key_Enter]:
            self.returnPressed.emit()
        elif event.key() in [QtCore.Qt.Key_Escape]: 
            self.hideWanted.emit()
        elif event.key() == QtCore.Qt.Key_L:
            self.openWanted.emit()
        elif event.modifiers()==QtCore.Qt.ControlModifier:
            if event.key() in [QtCore.Qt.Key_BracketLeft]:
                self.hideWanted.emit()
            elif event.key() in  [QtCore.Qt.Key_M, 
                                  QtCore.Qt.Key_Return, 
                                  QtCore.Qt.Key_Enter]:
                self.returnPressed.emit()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

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

        if not row: row=self.currentRow()

        for i in range(self.count()):
            if i==row: return self.itemWidget(self.item(i))

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
