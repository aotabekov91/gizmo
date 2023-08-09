from PyQt5 import QtCore

from ..base import Mode
from .widget import InputWidget

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

        self.widget=InputWidget(self.app.main)
        self.widget.hide()

    def showField(self, field=True, label=False):

        self.widget.show()
        if field:
            self.widget.field.show()
        if label:
            self.widget.label.show()

        self.widget.field.setFocus()

    def hideClearField(self):

        self.widget.hide()
        self.widget.label.hide()
        self.widget.field.hide()

        self.widget.field.clear()
        self.widget.label.clear()

    def eventFilter(self, widget, event):

        if self.listening:

            if  event.type()==QtCore.QEvent.Enter:

                event.accept()
                return True

            elif  event.type()==QtCore.QEvent.KeyPress:

                m=(event.modifiers() and event.modifiers()==QtCore.Qt.ControlModifier)

                enter=m and event.key()==QtCore.Qt.Key_M
                escape=event.key()==QtCore.Qt.Key_Escape
                escape= escape or (m and event.key()==QtCore.Qt.Key_BracketLeft)

                if enter: 

                    self.on_returnPressed()
                    event.accept()
                    return True
                        
                elif escape: 

                    self.on_escapePressed()
                    event.accept()
                    return True

        return False 

    def on_escapePressed(self):

        if self.widget.isVisible(): self.hideClearField()
        self.forceDelisten.emit()

    def on_returnPressed(self):

        self.returnPressed.emit()
