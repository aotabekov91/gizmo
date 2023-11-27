from PyQt5 import QtCore
from gizmo.widget import TableWidget
from gizmo.vimo.item.mixin import ListWidgetItem 

from .wtable import WTableModel

class RTableModel(WTableModel):

    show_row=0
    row_map={}

    def load(self):

        rs=self.getTableRows()
        if self.show_row<len(rs):
            d=rs[self.show_row]
            self.m_data=d
            self.m_id=d.pop(self.uid)
            for k, v in self.row_map.items():
                data={'id': k.title(), k: d[k]}
                super().createElement(k, data)
            self.loaded.emit(self)

    def createListItem(self, e):

        k=e.index()
        v=self.row_map[k]
        l=self.list_item_class()
        w=self.widget_class(
                item=l, 
                element=e, 
                wmap={'id': {}, k: v},
                )
        e.setWidget(w)
        l.setElement(e)
        e.setListItem(l)
        return e

    @classmethod
    def isCompatible(cls, s, **kwargs):

        c=s and s==cls.pattern
        if not c: return
        c=kwargs.get('config', {})
        return c.get('row_map', False)

    def updateTableRow(self, e):

        if self.table:
            idx=e.index()
            data=e.data()
            c={self.uid: self.m_id}
            d={idx: data[idx]} 
            self.table.updateRow(c, d)
            return e
        return None

    def updateElement(self, e, data):

        if self.table:
            self.m_data.update(data)
            self.updateTableRow(e)
            self.elementUpdated.emit(e)
            return e
        return None
