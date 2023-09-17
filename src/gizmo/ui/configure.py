from plug import Plug 

class Configure(Plug):

    def __init__(self, 
                 app, 
                 parent, 
                 *args,
                 mode_keys={}, 
                 **kwargs): 

        self.app=app
        self.object=parent
        self.mode_keys=mode_keys
        self.object.modeKey=self.modeKey

        super().__init__(*args, **kwargs)

        self.setSettings()
        self.register()

    def setActions(self): super().setActions(obj=self.object)

    def modeKey(self, mode): return self.mode_keys.get(mode, '')

    def getSettings(self): return self.settings

    def setSettings(self):

        self.settings=None
        if self.app.config.get(f'{self.name}'):
            self.settings=self.app.config[f'{self.name}']

    def register(self):

        self.app.plugman.register(self.object, self.actions)
