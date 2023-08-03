from .base import Mode

class Command(Mode):

    def __init__(self, 
                 app, 
                 name='command',
                 listen_leader=',',
                 show_statusbar=True, 
                 delisten_wanted='normal',
                 **kwargs,
                 ):

        super(Command, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                show_statusbar=show_statusbar, 
                **kwargs,
                )

    def _onExecuteMatch(self):

        if self.delisten_wanted: 
            self.app.modes.setMode(self.delisten_wanted)
