from PyQt5 import QtWidgets, QtCore

from .base import Plug

class PlugWidget(Plug, QtWidgets.QWidget):

    def activate(self):

        if not self.activated:
            self.activated=True
            self.show()

    def deactivate(self):

        if self.activated:
            self.activated=False
            self.hide()

    def keyPressEvent(self, event):

        if event.key()==QtCore.Qt.Key_Escape:
            self.deactivate()
        else:
            super().keyPressEvent(event)
