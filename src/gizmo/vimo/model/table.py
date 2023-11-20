from PyQt5 import QtCore
from gizmo.vimo.element import Element

from .base import Model

class TableModel(Model):

    uid='id'
    m_rows={}
    table=None
    kind='table'
    element_class=Element
    elementAdded=QtCore.pyqtSignal(object)
    elementRemoved=QtCore.pyqtSignal(object)
    elementUpdated=QtCore.pyqtSignal(object)
    elementAddWanted=QtCore.pyqtSignal(object)
    elementRemoveWanted=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
        self.elementRemoveWanted.connect(
                self.removeElement)
        self.elementUpdated.connect(
                self.updateRow)

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

    def find(self, idx, by='id'):

        for e in self.m_elements.values():
            d=e.data()
            if idx==d.get(by, None):
                return e

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

    def updateRow(self, e):

        idx=e.index()
        d={self.uid: idx}
        self.table.updateRow(d, e.data())

    def removeRow(self, e):

        idx=e.index()
        d={self.uid: idx}
        self.table.removeRow(d)

    def removeElement(self, e):

        self.removeRow(e)
        self.m_elements.pop(e.index())
        self.elementRemoved.emit(e)
