from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .mode import Modes
from .buffer import Buffer
from .plug import Plugs

class Manager(QObject):

    bufferCreated=pyqtSignal(object)

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

        if not mode: mode=Modes
        self.app.modes=mode(self.app)

    def setPlugManager(self, plug):

        if not plug: plug=Plugs
        self.app.plugs=plug(self.app)

    def setBufferManager(self, buffer): 

        if not buffer: buffer=Buffer
        self.app.buffer=buffer(self.app)
        self.app.buffer.bufferCreated.connect(self.bufferCreated)
