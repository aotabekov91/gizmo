from PyQt5 import QtWidgets, QtCore

class ListView(QtWidgets.QListView):

    def __init__(
            self, *args, **kwargs): 

        super().__init__(
                *args, **kwargs)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

    def currentItem(self):

        m=self.model()
        if m:
            if hasattr(m, 'itemFromIndex'):
                return m.itemFromIndex(
                        self.currentIndex())
            elif type(m)==QtCore.QSortFilterProxyModel:
                index=m.mapToSource(
                        self.currentIndex())
                return m.itemFromIndex(index)
