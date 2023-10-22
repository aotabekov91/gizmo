from PyQt5 import QtWidgets, QtCore, QtGui

class Delegate(QtWidgets.QItemDelegate):

    def paint(self, painter, opt, idx):

        painter.save()
        proxy=idx.model()
        model=proxy.sourceModel()
        index=proxy.mapToSource(idx)
        item=model.itemFromIndex(index)
        if item:
            item.widget.render(
                    painter, 
                    QtCore.QPoint(), 
                    QtGui.QRegion(), 
                    QtWidgets.QWidget.DrawChildren
                    )
        painter.restore()
