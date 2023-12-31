from PyQt5 import QtCore, QtWidgets, QtGui

from .proxy import ProxyModel
from .delegate import Delegate
from ..items import IconUpDown

class ListView(QtWidgets.QListView):

    hideWanted=QtCore.pyqtSignal()
    itemChanged=QtCore.pyqtSignal()
    openWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            *args,
            objectName='List', 
            item_widget=IconUpDown, 
            item_position='PositionAtCenter', 
            **kwargs
            ):

        self.item_widget=item_widget
        self.item_position=item_position
        super().__init__(
                objectName=objectName,
                )
        self.setup()
        self.setupUI()

    def setup(self):

        self.proxy=ProxyModel()
        self.setModel(self.proxy)
        self.setItemDelegate(Delegate())
        self.source=QtGui.QStandardItemModel()
        self.proxy.setSourceModel(self.source)

    def setupUI(self):

        self.setSpacing(2)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)

    def setList(self, dlist=[], limit=30, **kwargs):

        self.proxy.clear()
        self.source.clear()
        for i, data in enumerate(dlist):
            w = self.item_widget(self, data) 
            self.source.appendRow(w.item)

    def adjustSize(self, *args, **kwargs):
        super().adjustSize()
