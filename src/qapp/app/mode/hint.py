from .base import Mode 

class Hint(Mode):

    def __init__(self, 
                 app,
                 name='hint',
                 listen_leader='f',
                 show_statusbar=True,
                 delisten_on_exec=True,
                 **kwargs,
                 ):

        super().__init__(app, 
                         name=name,
                         listen_leader=listen_leader,
                         show_statusbar=show_statusbar,
                         delisten_on_exec=delisten_on_exec,
                         **kwargs,
                         )

        self.hints=None

    def activateCheck(self, event):

        leaderPressed=super().activateCheck(event)
        if leaderPressed:
            return self.app.modes.normal.listening
