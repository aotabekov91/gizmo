from PyQt5 import QtCore
from gizmo.vimo.model.base import Model
from gizmo.vimo.element import TableElement

class TableModel(Model):

    element_class=TableElement
    elementAdded=QtCore.pyqtSignal(object)
    elementRemoved=QtCore.pyqtSignal(object)
    elementUpdated=QtCore.pyqtSignal(object)

    def setup(self):

        self.m_rows={}
        super().setup()
        self.m_listwidget=None
        self.m_uid=self.kwargs.get(
                'uid', 'id')
        self.m_table=self.kwargs.get(
                'table', None)

    def listWidget(self):
        return self.m_listwidget

    def setListWidget(self, listwidget=None):
        self.m_listwidget=listwidget

    def getTableRows(self):
        return self.m_table.getRow(self.m_id)

    def load(self):

        for row in self.getTableRows():
            self.createElement(
                    row[self.m_uid], row)
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
        return self.m_table.getRow(data)

    def addTableRow(self, data):

        idx=self.m_table.writeRow(data)
        rs=self.getTableRow({self.m_uid:idx})
        return rs[0]

    def updateTableRow(self, e):

        idx=e.index()
        d={self.m_uid: idx}
        self.m_table.updateRow(d, e.data())
        return e

    def removeTableRow(self, e):

        idx=e.index()
        d={self.m_uid: idx}
        self.m_table.removeRow(d)
        return e

    def updateElement(self, e, data):

        e.m_data.update(data)
        self.updateTableRow(e)
        self.elementUpdated(e)
        return e

    def removeElement(self, e):

        self.removeTableRow(e)
        self.m_elements.pop(e.index())
        self.elementRemoved.emit(e)
        return e

    def addElement(self, data):

        data=self.addTableRow(data)
        idx=data[self.m_uid]
        e=self.createElement(idx, data)
        self.elementAdded.emit(e)
        return e
