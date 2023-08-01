import zmq

from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug

from ..utils import ZMQListener, KeyListener

class Plug(BasePlug):

    def __init__(self, 
                 app=None, 
                 listen_port=True,
                 command_leader=['.'],
                 command_activated=False,
                 **kwargs,
                 ):

        self.app=app

        self.actions={}
        self.commandKeys={}

        self.listen_port=listen_port
        self.command_leader=command_leader
        self.command_activated=command_activated

        super(Plug, self).__init__(**kwargs)

        self.setShortcuts()
        self.registerActions()

    def addLeader(self, leader):

        if not leader in self.command_leader:
            self.command_leader+=[leader]

    def setListener(self):

        self.listener = QtCore.QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(self.listener)
        self.listener.started.connect(self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(self.handle)
        QtCore.QTimer.singleShot(0, self.listener.start)

    def setOSListener(self):

        self.os_thread = QtCore.QThread()
        self.os_listener=KeyListener(self)
        self.os_listener.moveToThread(self.os_thread)
        self.os_thread.started.connect(self.os_listener.loop)
        QtCore.QTimer.singleShot(0, self.os_thread.start)

    def setConnection(self, exit=True, kind=zmq.PULL):

        if self.port or self.listen_port:

            try:
                self.socket = zmq.Context().socket(kind)
                if self.port:
                    self.socket.bind(f'tcp://*:{self.port}')
                elif self.listen_port:
                    self.port=self.socket.bind_to_random_port('tcp://*')
            except:
                self.socket=None

    def setShortcuts(self):

        if self.config.has_section('Shortcuts'):
            config=dict(self.config['Shortcuts'])
            for func_name, key in config.items():
                func=getattr(self, func_name, None)
                if func:
                    shortcut=QtWidgets.QShortcut(key)
                    shortcut.activated.connect(func)
                    self.action[(key, func_name)]=func

    def registerActions(self):

        if hasattr(self, 'ui'):
            for name in self.ui.__dir__():
                method=getattr(self.ui, name)
                if hasattr(method, 'key'):
                    if not method.info: method.info=name
                    if not method.key or not method.key in self.commandKeys:
                        self.actions[(method.key, method.info)]=method

        for name in self.__dir__():
            method=getattr(self, name)
            if hasattr(method, 'key'):
                if not getattr(method, 'info', None): 
                    method.__func__.info=name
                    if not method.key or not method.key in self.commandKeys:
                        self.commandKeys[method.key]=method
                        # self.actions[(method.key, method.info)]=method.__func__
                        self.actions[(method.key, method.info)]=method 

        if self.config.has_section('Keys'):
            config=dict(self.config['Keys'])
            for name, key in config.items():
                method=getattr(self, name, None)
                if method:
                    setattr(method.__func__, 'key', key)
                    setattr(method.__func__, 'info', name)
                    if not method.key or not method.key in self.commandKeys:
                        self.commandKeys[method.key]=method
                        self.actions[(method.key, method.info)]=method 

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.KeyPress:

            if self.command_leader:
                if event.text() in self.command_leader and not self.command_activated:
                    self.leader_pressed=event.text()
                    self.activateCommandMode()
                    return True
                elif event.text() in self.command_leader and self.command_activated:
                    self.deactivateCommandMode()
                    return True

        return super().eventFilter(widget, event)

    def deactivateCommandMode(self):

        self.leader_pressed=None
        self.command_activated=False
        if hasattr(self, 'ui') and hasattr(self.ui, 'commands'):
            if self.ui.current==self.ui.commands: 
                self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        self.command_activated=True
        if hasattr(self, 'ui') and hasattr(self.ui, 'commands'):
            self.ui.show(self.ui.commands)
