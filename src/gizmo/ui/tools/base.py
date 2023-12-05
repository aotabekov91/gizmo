from PyQt5 import QtCore 

from .tool import Tool

class Tools(QtCore.QObject):

    def __init__(self, window):

        super().__init__(
                parent=window)
        self.tools=[]
        self.current=None
        self.m_window=window
        self.createTools()

    def createTools(self):

        locs = {
                'up': QtCore.Qt.TopToolBarArea,
                'left': QtCore.Qt.LeftToolBarArea,
                'down': QtCore.Qt.BottomToolBarArea,
                'right': QtCore.Qt.RightToolBarArea,
                }

        for loc, r in locs.items():
            d = Tool()
            self.m_window.addToolBar(r, d)
            setattr(self, f'{loc}', d)
            self.tools+=[d]
            d.hide()
