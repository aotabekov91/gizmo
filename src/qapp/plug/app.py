import sys

from PyQt5 import QtWidgets

from .base import Plug

class PlugApp(Plug, QtWidgets.QApplication):

    def __init__(self, **kwargs):

        super(PlugApp, self).__init__(argv=[], **kwargs)

    def setName(self):

        super().setName()
        self.setApplicationName(self.name)

    def run(self):

        self.running=True
        sys.exit(self.exec_())

    def exit(self): 

        self.running=False
        sys.exit()
