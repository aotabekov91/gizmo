from PyQt5 import QtWidgets, QtCore

class Delegate(QtWidgets.QItemDelegate):

    def paint(self, painter, option, index):

        painter.save()
        item=self.model().item(index)
        item.widget.render(
                painter, 
                QtCore.QPoint(), 
                QtCore.QRegion(), 
                QtWidgets.QWidget.DrawChildren
                )
        painter.restore()
