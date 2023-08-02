from .base import Plug 

from types import MethodType, BuiltinFunctionType

class Configure(Plug):

    def __init__(self, app, name, parent, **kwargs): 

        self.object=parent
        self.object.modeKey=self.modeKey

        super().__init__(app=app, name=name, **kwargs)

        self.setSettings()

    def getSettings(self): return self.settings

    def setSettings(self):

        self.settings=None
        if self.app.config.has_section(f'{self.name}'):
            self.settings=self.app.config[f'{self.name}']

    def setActions(self):

        for name in self.object.__dir__():
            method=getattr(self.object, name)
            if type(method) in [MethodType, BuiltinFunctionType]:
                if hasattr(method, 'modes'):
                    data=(self.name, method.name)
                    if not data in self.actions:
                        self.actions[data]=method 
                        self.commandKeys[method.key]=method

    def registerActions(self):

        self.setActions()
        self.app.manager.register(self.object, self.actions)