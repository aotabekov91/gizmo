from gizmo.vimo.element import TableElement
from PyQt5.QtWidgets import QListWidgetItem
from gizmo.vimo.item.lwidget import BaseListWidget

from .stable import STableModel

class WTableModel(STableModel):

    element_class=TableElement
    widget_class=BaseListWidget

    def addItem(self, e):

        super().addItem(e)
        l=QListWidgetItem()
        w=self.widget_class(e)
        e.setWidget(w)
        e.setListItem(l)
