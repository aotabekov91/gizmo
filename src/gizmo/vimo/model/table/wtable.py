from PyQt5 import QtCore
from gizmo.widget import TableWidget
from gizmo.vimo.element import TableElement
from gizmo.vimo.item.mixin import ListWidgetItem 

from .stable import STableModel

class WTableModel(STableModel):

    widget_map={}
    widget_class=TableWidget
    list_item_class=ListWidgetItem
    listItemAdded=QtCore.pyqtSignal(object)

    def addElement(self, data):

        e=super().addElement(data)
        self.createListItem(e)
        self.listItemAdded.emit(e)

    def createElement(self, idx, data):

        e=super().createElement(idx, data)
        self.createListItem(e)
        return e

    def createListItem(self, e):

        l=self.list_item_class()
        w=self.widget_class(
                element=e, 
                listitem=l,
                widgetmap=self.widget_map,
                )
        e.setWidget(w)
        l.setElement(e)
        e.setListItem(l)
        return l
