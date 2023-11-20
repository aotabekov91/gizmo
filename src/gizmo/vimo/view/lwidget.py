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

        self.reconnect('disconnect')
        super().setModel(m)
        if m:
            print(m.m_elements)
            for i in range(m.rowCount()):
                m=self.m_model
                r=m.index(i, 0)
                e=m.itemFromIndex(r).element()
                self.addElement(e)
        self.reconnect()

    def addElement(self, e):

        print(self.name(), e.m_data)
        litem=e.listItem()
        self.addItem(litem)
        self.setItemWidget(
                litem, e.widget())

    def reconnect(self, kind='connect'):

        m=self.m_model
        if m:
            for f in [
                     'listItemAdded',
                     'elementRemoved',
                     ]:
                s=getattr(m, f, None)
                if not s: continue
                c=getattr(s, f, None)
                if not c: continue
                a=getattr(self, f'on_{f}', None) 
                if a: c(a)

    def on_listItemAdded(self, e):
        self.addElement(e)

    def on_elementRemoved(self, e):

        row=self.row(e.listItem())
        self.takeItem(row)
