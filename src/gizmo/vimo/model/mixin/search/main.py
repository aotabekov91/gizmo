from PyQt5 import QtCore

class Search:

    canSearch=True
    searchFound=QtCore.pyqtSignal(
            object, object)

    def search(self, *args, **kwargs):
        pass
