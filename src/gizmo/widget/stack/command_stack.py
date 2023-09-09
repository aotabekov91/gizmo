from PyQt6 import QtCore

from ..base import StackWidget
from ..compound import CommandList

class CommandStack(StackWidget):

    commandExecuted=QtCore.pyqtSignal()

    def __init__(self):

        super(CommandStack, self).__init__()
        super().addWidget(CommandList(), 'commands')
        self.commands.commandExecuted.connect(
                self.commandExecuted)

    def toggleCommands(self):

        if self.current==self.commands:
            if self.previous!=self.commands:
                self.show(self.previous)
            else:
                self.show(self.main)
        else:
            self.show(self.commands)
