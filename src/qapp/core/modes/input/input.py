from PyQt5 import QtCore, QtWidgets

from ..base import Mode
from .widget import InputWidget

class Input(Mode):

    escapePressed=QtCore.pyqtSignal()

    def __init__(self, 
                 app=None, 
                 name='input',
                 #Bug Ctrl+letter does not work
                 listen_leader='Ctrl+;',  
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

        self.edit=None
        self.widget=InputWidget(self.app)
        self.widget.hide()

    def listen(self):

        super().listen()
        self.showField()

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

    def eventFilter(self, w, e):

        if self.listening:
            if  e.type()==QtCore.QEvent.Enter:
                e.accept()
                return True
            elif  e.type()==QtCore.QEvent.KeyPress:
                m=e.modifiers()
                m=m and e.modifiers()==QtCore.Qt.ControlModifier
                enter=m and e.key()==QtCore.Qt.Key_M
                escape= e.key()==QtCore.Qt.Key_BracketLeft
                if enter or escape: 
                    if enter: 
                        self.on_returnPressed()
                    else:
                        self.on_escapePressed()
                    if self.widget.isVisible(): self.hideClearField()
                    e.accept()
                    self.client=None
                    self.forceDelisten.emit()
                    return True
        elif e.type()==QtCore.QEvent.KeyPress:
            mode=self.checkListen(e)
            if mode==self: 
                self.client=QtWidgets.QApplication.focusWidget()
                self.modeWanted.emit(mode)
                e.accept()
                return True
        return False 

    def setText(self):

        print(self.client)
        if self.client:
            func=None

            if not func:
                func=getattr(self.client, 'setText', None)
            if not func:
                func=getattr(self.client, 'setPlainText', None)

            if func: 
                text=self.widget.field.text()
                print(text)
                func(text)

    def on_escapePressed(self): pass


    def on_returnPressed(self): 

        self.setText()
        self.returnPressed.emit()
