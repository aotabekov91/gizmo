from PyQt5 import QtCore
from gizmo.widget import TableWidget
from gizmo.vimo.item.mixin import ListWidgetItem 

from .stable import STableModel

class WTableModel(STableModel):

    widget_class=TableWidget
    list_item_class=ListWidgetItem

    def removeElement(self, e):

        super().removeElement(e)
        w=self.listWidget()
        if w: w.removeElement(e)

    def addElement(self, data):

        e=super().addElement(data)
        print(e)
        w=self.listWidget()
        if w: w.addElement(e)
        self.createListItem(e)

    def createElement(self, idx, data):

        e=super().createElement(idx, data)
        return self.createListItem(e)

    def createListItem(self, e):

        l=self.list_item_class()
        w=self.widget_class(
                item=l,
                element=e, 
                wmap=self.widget_map,
                )
        e.setWidget(w)
        l.setElement(e)
        e.setListItem(l)
        return e
