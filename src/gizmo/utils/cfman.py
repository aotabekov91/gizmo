from PyQt5 import QtCore

class CFMan(QtCore.QObject):

    def __init__(
            self, 
            obj=None, 
            config={},
            **kwargs
            ):

        super().__init__(obj)
        self.obj=obj
        self.config=config
        self.kwargs=kwargs
        self.setup()

    def setup(self):
        raise
