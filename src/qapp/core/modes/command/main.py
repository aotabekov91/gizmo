from ..base import Mode
from .widget import CommandWindow

class Command(Mode):

    def __init__(self, 
                 app, 
                 name='command',
                 listen_leader=',',
                 show_statusbar=True, 
                 show_commands=False, 
                 **kwargs,
                 ):

        super(Command, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                show_commands=show_commands, 
                show_statusbar=show_statusbar, 
                **kwargs,
                )

    def setUI(self):
        
        self.ui=CommandWindow(self.app)

        self.ui.mode.hideWanted.connect(self.deactivate)
        self.ui.mode.returnPressed.connect(self.confirm)
        self.ui.mode.installEventFilter(self)

    def _onExecuteMatch(self):

        if self.delisten_wanted: 
            self.app.modes.setMode(self.delisten_wanted)
