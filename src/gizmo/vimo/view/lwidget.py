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

        super().setModel(m)
        if m:
            for i in range(m.rowCount()):
                m=self.m_model
                r=m.index(i, 0)
                i=m.itemFromIndex(r)
                e=i.element()
                self.addItem(e.listItem())
                self.setItemWidget(
                        e.listItem(),
                        e.widget())
