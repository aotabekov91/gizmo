from PyQt5 import QtCore

class Search:

    canSearch=True
    searchFounded=QtCore.pyqtSignal(
            object, object)

    def search(self, *args, **kwargs):
        pass
