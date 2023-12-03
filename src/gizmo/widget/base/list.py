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

    def currentItem(self, idx=None):

        m=self.model()
        if m:
            idx= idx or self.currentIndex()
            if type(m)==QtCore.QSortFilterProxyModel:
                idx=m.mapToSource(idx)
            if hasattr(m, 'itemFromIndex'):
                return m.itemFromIndex(idx)
