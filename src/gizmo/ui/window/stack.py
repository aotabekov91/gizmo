from PyQt5 import QtWidgets, QtCore

from gizmo.widget import StackWidget
from gizmo.ui.docks import Docks
from gizmo.ui.window import MainWindow
from gizmo.ui.statusbar import StatusBar

class StackWindow(QtWidgets.QMainWindow):

    windowResized=QtCore.pyqtSignal()

    def __init__(self):

        super().__init__()
        self.stack=StackWidget(
                objectName='StackedWindow')
        self.setCentralWidget(self.stack)
        self.setContentsMargins(
                0, 0, 0, 0)
        self.centralWidget().layout().setContentsMargins(
                0,0,0,0)
        self.setUI()

    def setUI(self):

        self.docks=Docks(self)
        self.bar=StatusBar(self)
        self.setStatusBar(self.bar)
        self.main=MainWindow()
        self.stack.addWidget(
                self.main, 'main', main=True)
        self.bar.hide()

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.windowResized.emit()
