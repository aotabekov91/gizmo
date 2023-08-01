from PyQt5.QtCore import *

class Modes(QObject):

    def __init__(self, app):

        super().__init__(app)

        self.app=app
        self.current=None

        self.modes=[]
        self.leaders={}

    def load(self): pass

    def getModes(self): return self.modes

    def addMode(self, mode):

        mode.setData()
        self.modes+=[mode]
        setattr(self, mode.name, mode) 

        mode.listenWanted.connect(self.setMode)
        mode.delistenWanted.connect(self.setMode)

        if mode.listen_leader: 
            self.leaders[mode.listen_leader]=mode

    def delisten(self): 

        for m in self.modes: m.delisten()

    def setMode(self, mode='normal'):

        self.delisten()

        if mode!='normal':
            if self.current and self.current.name==mode:
                mode='normal'
                
        self.current=getattr(self, mode, None)
        if self.current: self.current.listen()
