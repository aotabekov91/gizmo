from .base import Mode

class Input(Mode):

    def __init__(self, 
                 app, 
                 name='input',
                 listen_leader='i', 
                 show_statusbar=True, 
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

    def activateCheck(self, event):

        leaderPressed=super().activateCheck(event)
        if leaderPressed: 
            if self.app.modes.normal.listening:
                return len(self.app.modes.normal.keys_pressed)==0
