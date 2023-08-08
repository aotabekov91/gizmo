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


            m=event.modifiers()==QtCore.Qt.ControlModifier

            enter=m and QtCore.Qt.Key_M
            escape=event.key()==QtCore.Qt.Key_Escape
            escape= escape or (m and event.key()==QtCore.Qt.Key_BracketLeft)

            if enter: 

                self.returnPressed.emit()
                event.accept()
                return True
                    
            elif escape: 

                self.forceDelisten.emit()
                event.accept()
                return True

        return False
