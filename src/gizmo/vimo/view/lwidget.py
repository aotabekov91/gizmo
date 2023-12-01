from gizmo.vimo.view import mixin
from gizmo.widget import ListWidget

from .base import View

class ListWidgetView(
        mixin.WidgetGo,
        View,
        ListWidget,
        ):

    def setModel(self, model=None, **kwargs):

        if self.m_model==model: return
        super().setModel(model)
        if not model: return
        self.setListWidget()
        for i in range(model.rowCount()):
            model=self.m_model
            r=model.index(i, 0)
            e=model.itemFromIndex(r).element()
            self.addElement(e)
            self.setListWidget(self)

    def setListWidget(self, widget=None):

        if self.m_model: 
            self.m_model.setListWidget(
                    widget)

    def addElement(self, e):

        i=e.listItem()
        self.addItem(i)
        self.setItemWidget(i, e.widget())

    def removeElement(self, e):

        row=self.row(e.listItem())
        self.takeItem(row)
