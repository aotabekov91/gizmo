from gizmo.vimo.view import mixin
from gizmo.widget import ListWidget

from .base import View

class ListWidgetView(
        mixin.Input,
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
        first=None
        current=False
        for i in range(model.rowCount()):
            r=model.index(i, 0)
            e=model.itemFromIndex(r).element()
            current=self.addElement(e)
            if i==0: first=e
            model.setListWidget(self)
        if not current and first:
            l=first.listItem()
            self.setCurrentItem(l)

    def addElement(self, e):

        i=e.listItem()
        self.addItem(i)
        i.setHidden(False)
        ci=getattr(i, 'm_current_idx', False)
        self.setItemWidget(i, e.widget())
        if ci: 
            self.setCurrentItem(i)
            return True

    def cleanUp(self):

        m=self.m_model
        if not m: return
        ci=self.currentItem()
        for i in range(m.rowCount()):
            r=m.index(i, 0)
            e=m.itemFromIndex(r).element()
            l=e.listItem()
            l.setHidden(True)
            l.m_current_idx=ci==l

    def setListWidget(self, widget=None):

        if self.m_model: 
            self.m_model.setListWidget(
                    widget)

    def removeElement(self, e):

        i=e.listItem()
        self.takeItem(self.row(i))
