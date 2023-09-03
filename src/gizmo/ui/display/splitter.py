from PyQt5 import QtWidgets
from .base import BaseDisplay

class SplitterDisplay(BaseDisplay, QtWidgets.QSplitter):

    def __init__(self, 
                 app, 
                 window, 
                 view_class=None):

        super().__init__(parent=window)
        self.setup(app, window, view_class)
