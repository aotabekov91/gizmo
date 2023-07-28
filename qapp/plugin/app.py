import sys

from PyQt5 import QtWidgets

from .base import Plug

class PlugApp(Plug, QtWidgets.QApplication):

    def setName(self):

        super().setName()
        self.setApplicationName(self.name)

    def run(self):

        self.running=True
        self.setListener()
        sys.exit(self.exec_())

    def exit(self): 

        self.running=False
        sys.exit()

if __name__=='__main__':
    app=PlugApp(port=33333)
    app.run()
