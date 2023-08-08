from PyQt5 import QtCore

class Modeman(QtCore.QObject):

    def __init__(self, app):

        super().__init__(app)

        self.app=app
        self.modes=[]
        self.current=None

    def load(self): pass

    def getModes(self): return self.modes

    def reportToBar(self, digit=None, key=None):

        if self.current:
            if getattr(self.current, 'report_keys', False):
                data={'mode':self.current.name.title(), 
                      'detail':''.join(
                          self.current.keys_pressed)}
                self.app.main.bar.setData(data)

    def addMode(self, mode):

        if hasattr(mode, 'setPlugData'): mode.setPlugData()

        self.modes+=[mode]
        setattr(self, mode.name, mode) 

        mode.modeWanted.connect(self.setMode)
        mode.forceDelisten.connect(self.setMode)
        mode.keyPressed.connect(self.reportToBar)
        mode.delistenWanted.connect(self.on_delistenWanted)

    def on_delistenWanted(self):

        if not self.current.name!='input':
            self.setMode()

    def setMode(self, mode='normal'):

        if self.current: self.current.delisten()

        if type(mode)==str:
            mode=getattr(self, mode, 'normal')

        self.current=mode
        self.reportToBar()

        self.current.listen()
        if self.current.name=='normal':
            self.app.main.setFocus()

        data={'mode':self.current.name.title()} 
        self.app.main.bar.setData(data)
