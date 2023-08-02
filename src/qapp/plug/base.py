import zmq

from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug

from ..utils import ZMQListener, KeyListener

class Plug(BasePlug):

    respond=QtCore.pyqtSignal(dict)

    def __init__(self, 
                 app=None, 
                 command_leader=['.'],
                 command_activated=False,
                 **kwargs,
                 ):

        self.app=app
        self.command_leader=command_leader
        self.command_activated=command_activated

        super(Plug, self).__init__(**kwargs)

        self.setShortcuts()

    def addLeader(self, leader):

        if not leader in self.command_leader:
            self.command_leader+=[leader]

    def setListener(self):

        self.listener = QtCore.QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(self.listener)
        self.listener.started.connect(
                self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(self.act)
        QtCore.QTimer.singleShot(0, self.listener.start)

    def act(self, request):

        response=self.handle(request)
        if self.respond_port:
            self.socket.send_json(response)
        self.zeromq_listener.acted=True

    def setOSListener(self):

        self.os_thread = QtCore.QThread()
        self.os_listener=KeyListener(self)
        self.os_listener.moveToThread(self.os_thread)
        self.os_thread.started.connect(
                self.os_listener.loop)
        QtCore.QTimer.singleShot(0, self.os_thread.start)

    def setConnection(self, kind=zmq.PULL):

        super().setConnection(kind)
        if self.port or self.listen_port:
            self.setListener()

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
            for f in self.ui.__dir__():
                m=getattr(self.ui, f)
                if hasattr(m, 'key'):
                    if not m.info: m.info=f
                    if not m.key or not m.key in self.commandKeys:
                        self.actions[(m.key, m.info)]=m

        for f in self.__dir__():
            m=getattr(self, f)
            if hasattr(m, 'key'):
                if not getattr(m, 'info', None): 
                    m.__func__.info=f
                    if not m.key or not m.key in self.commandKeys:
                        self.commandKeys[m.key]=m
                        # self.actions[(method.key, method.info)]=method.__func__
                        self.actions[(m.key, m.info)]=m 

        if self.config.has_section('Keys'):
            config=dict(self.config['Keys'])
            for f, key in config.items():
                m=getattr(self, f, None)
                if m:
                    setattr(m.__func__, 'key', key)
                    setattr(m.__func__, 'info', f)
                    if not m.key or not m.key in self.commandKeys:
                        self.commandKeys[m.key]=m
                        self.actions[(m.key, m.info)]=m 

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
