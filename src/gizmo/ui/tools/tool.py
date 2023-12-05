from PyQt5 import QtWidgets

class Tool(QtWidgets.QToolBar):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        l=self.layout()
        self.setContentsMargins(0,0,0,0)
        l.setContentsMargins(0,0,0,0)
        self.setFloatable(False)
        self.setMovable(False)
        l.setSpacing(0)
