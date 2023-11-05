from PyQt5 import QtCore

class Search:

    canSearch=True
    searchFound=QtCore.pyqtSignal(
            object, object)

    def setModel(self, model):

        super().setModel(model)
        if self.checkModelProp('canSearch'):
            model.searchFound.connect(
                    self.on_searchFound)

    def on_searchFound(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass
