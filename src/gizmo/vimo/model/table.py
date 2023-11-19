from PyQt5 import QtCore
from gizmo.vimo.element import Element

from .base import Model

class TableModel(Model):

    uid='id'
    table=None
    kind='table'
    element_class=Element
    elementAddWanted=QtCore.pyqtSignal(object)
    elementRemoveWanted=QtCore.pyqtSignal(object)
    elementUpdateWanted=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
        self.elementRemoveWanted.connect(
                self.remove)

    def getRows(self):
        return self.table.getRow(self.m_id)

    def load(self):

        for row in self.getRows():
            idx=row[self.uid]
            e=self.element_class(
                    data=row,
                    index=idx,
                    model=self)
            self.m_elements[idx]=e
            self.elementCreated.emit(e)
        self.loaded.emit()

    def get(self, data):
        self.table.getRow(data)

    def add(self, data):

        idx=self.table.writeRow(data)
        data['id']=idx
        e=self.element_class(
                data=data,
                index=idx,
                model=self)
        self.elementCreated.emit(e)
        self.m_elements[idx]=e

    def remove(self, e):

        idx=e.index()
        d={self.uid: idx}
        self.table.removeRow(d)
        self.m_elements.pop(idx)
