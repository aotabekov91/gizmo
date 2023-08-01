from .base import Mode 

class Visual(Mode):

    def __init__(self, 
                 app,
                 name='visual',
                 listen_leader='v',
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

        self.hints=None
        self.hinting=False

    def activateCheck(self, event):

        leaderPressed=super().activateCheck(event)
        if leaderPressed:
            return self.app.modes.normal.listening
