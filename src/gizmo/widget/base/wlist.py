from PyQt5 import QtCore, QtWidgets

class ListWidget(QtWidgets.QListWidget):

    item_widget=None
    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            parent=None,
            objectName='ListWidget', 
            **kwargs
            ):

        super().__init__(
                parent=parent,
                objectName=objectName)
        self.setup()

    def setup(self):

        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)
        self.setResizeMode(QtWidgets.QListView.Adjust)
