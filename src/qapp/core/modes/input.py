from .base import Mode

class Input(Mode):

    def __init__(self, 
                 app=None, 
                 name='input',
                 listen_leader='Ctrl+i', 
                 delisten_on_exec=False,
                 **kwargs,
                 ):

        super().__init__(app=app, 
                         name=name,
                         listen_leader=listen_leader, 
                         delisten_on_exec=delisten_on_exec,
                         **kwargs,
                         )
