from PyQt5 import QtWidgets, QtCore, QtGui

from gizmo.ui.docks import Docks
from gizmo.widget import StackWidget
from gizmo.ui.window import MainWindow
from gizmo.ui.statusbar import StatusBar
from gizmo.ui.window.overlay import Overlay

class StackWindow(QtWidgets.QMainWindow):

    resized=QtCore.pyqtSignal()

    def __init__(
            self,
            *args, 
            **kwargs,
            ):

        super().__init__(*args, **kwargs)
        self.stack=StackWidget(
                parent=self,
                objectName='StackedWindow'
                )
        self.stack.resized.connect(
                self.resized)
        self.stack.resized.connect(
                self.on_stackResized)
        self.setCentralWidget(
                self.stack)
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
        self.overlay=Overlay(
                parent=self)
        self.stack.addWidget(
                self.main, 'main', main=True)
        self.bar.hide()

    def on_stackResized(self, event):

        self.overlay.resize(event.size())
        self.resized.emit()

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.overlay.resize(event.size())
        self.resized.emit()
