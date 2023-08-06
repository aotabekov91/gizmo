from .base import Mode

class Input(Mode):

    def __init__(self, 
                 app=None, 
                 name='input',
                 show_statusbar=True, 
                 listen_leader='Ctrl+i', 
                 delisten_on_exec=False,
                 **kwargs,
                 ):

        super().__init__(app=app, 
                         name=name,
                         listen_leader=listen_leader, 
                         show_statusbar=show_statusbar,
                         delisten_on_exec=delisten_on_exec,
                         **kwargs,
                         )

    def checkListen(self, event):

        leaderPressed=super().checkListen(event)
        if leaderPressed: 
            if self.app.modes.normal.listening:
                return len(self.app.modes.normal.keys_pressed)==0
