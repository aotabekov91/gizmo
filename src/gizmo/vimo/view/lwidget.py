from gizmo.vimo.view import mixin
from gizmo.widget import ListWidget

from .base import View

class ListWidgetView(
        mixin.WidgetGo,
        View,
        ListWidget,
        ):

    def setModel(self, model=None, **kwargs):

        if id(self.m_model)==id(model): 
            return
        self.cleanUp()
        self.setListWidget()
        super().setModel(model)
        for i in range(model.rowCount()):
            r=model.index(i, 0)
            e=model.itemFromIndex(r).element()
            self.addElement(e)
            model.setListWidget(self)

    def setItemWidget(self, item, widget):

        m=super(ListWidget, self).model()
        index=m.index(self.row(item))
        if widget: 
            widget.setParent(self.viewport())
            widget.installEventFilter(self)
            widget.show()
            self.dataChanged(index, index)

    def cleanUp(self):

        m=self.m_model
        if not m: return
        for i in range(m.rowCount()):
            r=m.index(i, 0)
            e=m.itemFromIndex(r).element()
            w=e.widget()
            w.setParent(None)
            w.removeEventFilter(self)
            w.hide()

    def setListWidget(self, widget=None):

        if self.m_model: 
            self.m_model.setListWidget(
                    widget)

    def addElement(self, e):

        i=e.listItem()
        self.addItem(i)
        self.setItemWidget(i, e.widget())

    def removeElement(self, e):

        i=e.listItem()
        self.takeItem(i.row())
