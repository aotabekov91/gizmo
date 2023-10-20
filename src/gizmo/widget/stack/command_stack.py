from PyQt5 import QtCore
from ..base import StackWidget
from ..compound import CommandList

class CommandStack(StackWidget):

    commandExecuted=QtCore.pyqtSignal()

    def __init__(
            self, 
            *args, 
            **kwargs
            ):

        super().__init__(
                *args, 
                **kwargs
                )
        c=CommandList()
        c.commandExecuted.connect(
                self.commandExecuted)
        self.addWidget(c, 'commands')

    def toggleCommands(self):

        if self.current==self.commands:
            if self.previous!=self.commands:
                self.show(self.previous)
            else:
                self.show(self.main)
        else:
            self.show(self.commands)
