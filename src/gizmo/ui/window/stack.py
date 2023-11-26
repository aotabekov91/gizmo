from PyQt5 import QtWidgets, QtCore, QtGui

from gizmo.ui.docks import Docks
from gizmo.ui.window import MainWindow
from gizmo.widget import StackedWidget
from gizmo.ui.statusbar import StatusBar
from gizmo.ui.window.overlay import Overlay

class StackWindow(QtWidgets.QMainWindow):

    resized=QtCore.pyqtSignal()
    focusGained=QtCore.pyqtSignal()
    stackResized=QtCore.pyqtSignal()
    windowResized=QtCore.pyqtSignal()

    def __init__(
            self,
            *args, 
            stack=None,
            objectName='StackedWindow',
            **kwargs,
            ):

        self.m_size=None
        super().__init__(
                *args, 
                objectName=objectName,
                **kwargs
                )
        self.setStack(stack)
        self.setupUI()

    def setStack(self, stack=None):

        if not stack:
            stack=StackedWidget(
                parent=self,
                objectName='StackedWidget',
                )
        self.stack=stack
        self.stack.resized.connect(
                self.resized)
        self.stack.resized.connect(
                self.on_stackResized)
        self.stack.resized.connect(
                self.stackResized)
        self.stack.focusGained.connect(
                self.focusGained)
        self.setCentralWidget(
                self.stack)
        self.setContentsMargins(
                0, 0, 0, 0)

    def setupUI(self):

        self.docks=Docks(self)
        self.bar=StatusBar(self)
        self.setStatusBar(self.bar)
        self.main=MainWindow(self)
        self.overlay=Overlay(self)
        self.stack.addWidget(
                self.main, 'main', True)
        self.bar.hide()

    def on_stackResized(self, event):

        s=self.size()
        self.overlay.resize(s)
        self.resizeEvent(event)
