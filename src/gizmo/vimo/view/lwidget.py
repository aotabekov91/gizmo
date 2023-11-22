from gizmo.vimo.view import mixin
from gizmo.widget import ListWidget

from .base import View

class ListWidgetView(
        mixin.WidgetGo,
        mixin.ViewMove,
        View,
        ListWidget,
        ):

    def setModel(self, m):

        self.setListWidget()
        super().setModel(m)
        if m:
            for i in range(m.rowCount()):
                m=self.m_model
                r=m.index(i, 0)
                e=m.itemFromIndex(r).element()
                self.addElement(e)
                self.setListWidget(self)

    def setListWidget(self, widget=None):

        m=self.m_model
        if m: m.setListWidget(widget)

    def addElement(self, e):

        i=e.listItem()
        self.addItem(i)
        self.setItemWidget(i, e.widget())

    def removeElement(self, e):

        row=self.row(e.listItem())
        self.takeItem(row)
