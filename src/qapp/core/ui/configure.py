from plug import Plug 

class Configure(Plug):

    def __init__(self, app, parent, mode_keys={}, **kwargs): 

        self.app=app
        self.object=parent
        self.mode_keys=mode_keys
        self.object.modeKey=self.modeKey

        super().__init__(listen_port=False, **kwargs)

        self.setSettings()
        self.setActions()
        self.registerActions()

    def modeKey(self, mode): return self.mode_keys.get(mode, '')

    def getSettings(self): return self.settings

    def setSettings(self):

        self.settings=None
        if self.app.config.has_section(f'{self.name}'):
            self.settings=self.app.config[f'{self.name}']

    def registerActions(self):

        self.app.manager.register(self.object, self.actions)