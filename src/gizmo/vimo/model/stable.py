from PyQt5.QtGui import QStandardItemModel
from gizmo.vimo.item.mixin import StandardItem

from .table import TableModel

class STableModel(
        QStandardItemModel,
        TableModel
        ):

    item_class=StandardItem

    def setup(self):

        super().setup()
        self.loaded.connect(self.connect)
        self.elementCreated.connect(self.addItem)

    def addItem(self, e):

        i=self.item_class()
        i.setElement(e)
        self.appendRow(i)
        return i

    def connect(self):

        self.rowsAboutToBeRemoved.connect(
                self.on_rowsAboutToBeRemoved)
        self.rowsAboutToBeInserted.connect(
                self.on_rowsAboutToBeInserted)

    def on_rowsAboutToBeRemoved(
            self, p, f, l):

        for j in range(f, l+1):
            idx=self.index(j, 0)
            i=self.itemFromIndex(idx)
            if i:
                e=i.element()
                self.elementRemoveWanted.emit(e)
            
    def on_rowsAboutToBeInserted(
            self, p, f, l):

        for j in range(f, l+1):
            idx=self.index(j, 0)
            i=self.itemFromIndex(idx)
            if i:
                e=i.element()
                self.elementAddWanted.emit(e)
