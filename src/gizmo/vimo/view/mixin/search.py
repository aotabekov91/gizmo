from PyQt5 import QtCore

class Search:

    canSearch=True
    searchWanted=QtCore.pyqtSignal(
            object)
    searchFound=QtCore.pyqtSignal(
            object, object)

    def setup(self):

        super().setup()
        self.modelIsToBeChanged.connect(
                self.on_modelIsToBeChanged)
        self.modelChanged.connect(
                self.on_modelChanged)
        self.searchWanted.connect(
                self.search)

    def on_modelIsToBeChanged(self, v, m):

        if self.checkModelProp('canSearch', m):
            m.searchFound.disconnect(
                    self.on_searchFound)

    def on_modelChanged(self, v, m):

        if self.checkModelProp('canSearch'):
            m.searchFound.connect(
                    self.on_searchFound)

    def on_searchFound(self, *args, **kwargs):
        raise

    def search(self, *args, **kwargs):
        raise
