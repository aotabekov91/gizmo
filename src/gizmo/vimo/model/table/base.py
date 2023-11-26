from PyQt5 import QtCore
from gizmo.vimo.model.base import Model
from gizmo.vimo.element import TableElement

class TableModel(Model):

    table=None
    element_class=TableElement
    elementAdded=QtCore.pyqtSignal(object)
    elementRemoved=QtCore.pyqtSignal(object)
    elementUpdated=QtCore.pyqtSignal(object)

    def setup(self):

        self.m_rows={}
        super().setup()
        self.m_listwidget=None

    def listWidget(self):
        return self.m_listwidget

    def setListWidget(self, listwidget=None):
        self.m_listwidget=listwidget

    def getTableRows(self):

        if self.m_id and self.table:
            return self.table.getRow(
                    self.m_id)
        return []

    def load(self):

        for row in self.getTableRows():
            self.createElement(
                    row[self.uid], row)
        self.loaded.emit()

    def createElement(self, idx, data):

        e=self.element_class(
                data=data,
                index=idx,
                model=self)
        self.m_elements[idx]=e
        self.elementCreated.emit(e)
        return e

    def findElement(self, cond, by='id'):

        for e in self.m_elements.values():
            d=e.data()
            if cond==d.get(by, None):
                return e

    def getTableRow(self, data):

        if self.table:
            return self.table.getRow(data)
        return []

    def addTableRow(self, data):

        if self.table:
            idx=self.table.writeRow(data)
            rs=self.getTableRow({self.uid:idx})
            return rs[0]
        return None

    def updateTableRow(self, e):

        if self.table:
            idx=e.index()
            d={self.uid: idx}
            self.table.updateRow(d, e.data())
            return e
        return None

    def removeTableRow(self, e):

        if self.table:
            idx=e.index()
            d={self.uid: idx}
            self.table.removeRow(d)
            return e
        return None

    def updateElement(self, e, data):

        if self.table:
            e.m_data.update(data)
            self.updateTableRow(e)
            self.elementUpdated.emit(e)
            return e
        return None

    def removeElement(self, e):

        self.removeTableRow(e)
        self.m_elements.pop(e.index())
        self.elementRemoved.emit(e)
        return e

    def addElement(self, data):

        data=self.addTableRow(data)
        idx=data[self.uid]
        e=self.element(idx)
        if e:
            e.setData(data)
            self.elementUpdated.emit(e)
        else:
            e=self.createElement(idx, data)
            self.elementAdded.emit(e)
        return e
