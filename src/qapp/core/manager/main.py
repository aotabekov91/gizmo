from PyQt5 import QtCore

from .modeman import Modeman
from .plugman import Plugman
from .buffman import Buffman

class Manager(QtCore.QObject):

    bufferCreated=QtCore.pyqtSignal(object)

    def __init__(self, app, buffer=None, mode=None, plug=None):

        super(Manager, self).__init__(app)

        self.app=app
        self.actions={}

        self.setModeManager(mode)
        self.setBufferManager(buffer)
        self.setPlugManager(plug)

    def register(self, plug, actions): 

        self.actions[plug]=actions
        self.app.actionRegistered.emit()

    def setModeManager(self, mode):

        if not mode: mode=Modeman
        self.app.modes=mode(self.app)

    def setPlugManager(self, plug):

        if not plug: plug=Plugman
        self.app.plugs=plug(self.app)

    def setBufferManager(self, buffer): 

        if not buffer: buffer=Buffman
        self.app.buffer=buffer(self.app)
        self.app.buffer.bufferCreated.connect(self.bufferCreated)