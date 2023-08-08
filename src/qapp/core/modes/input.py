from .base import Mode
from PyQt5 import QtCore

class Input(Mode):

    escapePressed=QtCore.pyqtSignal()

    def __init__(self, 
                 app=None, 
                 name='input',
                 listen_leader='Ctrl+i', 
                 delisten_on_exec=False,
                 **kwargs
                 ):

        super().__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader, 
                delisten_on_exec=delisten_on_exec, 
                **kwargs
                )

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.KeyPress
        if self.listening and c1: 

            enter=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]

            m=event.modifiers()==QtCore.Qt.ControlModifier
            escape=event.key()==QtCore.Qt.Key_Escape
            escape= escape or (m and event.key()==QtCore.Qt.Key_BracketLeft)

            if event.key() in enter: 

                self.returnPressed.emit()
                event.accept()
                return True
                    
            elif espace: 

                self.forceDelisten.emit()
                event.accept()
                return True

        return super().eventFilter(widget, event)
