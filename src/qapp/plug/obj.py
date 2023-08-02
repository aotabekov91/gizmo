from PyQt5 import QtWidgets, QtCore

from .base import Plug
from ..widget import BaseCommandStack 

class PlugObj(Plug, QtCore.QObject):

    def __init__(self,
                 mode_keys={},
                 position=None,
                 listen_port=False, 
                 **kwargs):

        super(PlugObj, self).__init__(
                listen_port=listen_port,
                **kwargs)

        self.position=position
        self.mode_keys=mode_keys
        self.registerActions()

    def setUI(self): 

        self.ui=BaseCommandStack(self, self.position)
        self.ui.focusGained.connect(self.actOnFocus)
        self.ui.focusLost.connect(self.actOnDefocus)

    def actOnDefocus(self): 

        self.deactivateCommandMode()
        self.app.modes.setMode('normal')

    def actOnFocus(self):

        self.setStatusbarData()
        self.app.modes.setMode('me')

    def setStatusbarData(self):

        self.data={
                'detail': '',
                'client': self,
                'visible': True, 
                'info': self.name.title()
                }
        self.app.main.bar.setData(self.data)

    def modeKey(self, mode): return self.mode_keys.get(mode, '')

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def activate(self):

        self.activated=True
        if hasattr(self, 'ui'): self.ui.activate()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): self.ui.deactivate()

    def setShortcuts(self):

        if self.config.has_section('Shortcuts'):
            shortcuts=dict(self.config['Shortcuts'])
            for func_name, key in shortcuts.items():
                func=getattr(self, func_name, None)
                if func and hasattr(func, 'widget'): 
                    if func.widget=='window':
                        widget=self.app.main
                    elif func.widget=='display':
                        widget=self.app.main.display
                    else:
                        setattr(func, 'key', key)
                        continue
                    context=getattr(func, 
                                    'context', 
                                    QtCore.Qt.WidgetWithChildrenShortcut)
                    shortcut=QtWidgets.QShortcut(widget)
                    shortcut.setKey(key)
                    shortcut.setContext(context)
                    shortcut.activated.connect(func)

    def registerActions(self):

        self.setActions()
        self.app.manager.register(self, self.actions)

    def keyPressEvent(self, event):

        if event.key()==QtCore.Qt.Key_Escape:
            self.deactivate()
        else:
            super().keyPressEvent(event)
