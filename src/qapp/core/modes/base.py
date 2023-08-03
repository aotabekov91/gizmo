import inspect

from PyQt5 import QtCore 

from ...plug import PlugObj
from ...utils import register
from ...widget import ListWidget 

class Mode(PlugObj):

    returnPressed=QtCore.pyqtSignal()
    listenWanted=QtCore.pyqtSignal(str)
    delistenWanted=QtCore.pyqtSignal(str)
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(self, 
                 wait_time=250,
                 listening=False,
                 listen_leader=None,
                 show_statusbar=False,
                 delisten_on_exec=True,
                 delisten_wanted='normal',
                 listen_widget=[],
                 exclude_widget=[],
                 **kwargs):

        self.commands=[]
        self.keys_pressed=[]
        self.wait_time=wait_time
        self.listening=listening

        self.listen_widget=listen_widget
        self.listen_leader=listen_leader
        self.exclude_widget=exclude_widget

        self.show_statusbar=show_statusbar
        self.delisten_wanted=delisten_wanted
        self.delisten_on_exec=delisten_on_exec

        super(Mode, self).__init__(command_leader=[], **kwargs)

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.delisten)

        self.setUI()
        self.setBarData()
        self.app.modes.addMode(self)

        self.app.installEventFilter(self)

    def setBarData(self):
        
        self.data={
                'detail': '',
                'client': self,
                'visible': self.show_statusbar,
                'info':f'[{self.name.title()}]',
                }

    def setData(self):

        self.commands=[]

        for plug, actions in self.app.manager.actions.items():
            self.setPlugData(plug, actions, self.name)

        #own actions
        self.setPlugData(self, self.app.manager.actions[self])

    def setPlugData(self, plug, actions, mname=None):

        for (pname, fname), method in actions.items():
            if not mname or  mname in method.modes:
                method_name=getattr(method, 'info', None)
                if method_name: fname=method_name
                name=f'[{pname}] {fname}'
                data={'id': method, 'up': name, 'plug': pname}
                if method.key: 
                    key=method.key
                    if hasattr(plug, 'modeKey'): 
                        prefix=plug.modeKey(self.name)
                        key=f'{prefix}{key}'
                    data['down']=key
                self.commands+=[data]

    def activate(self):

        self.app.modes.delisten()
        self.app.main.bar.setData(self.data)
        self.listening=True

    def confirm(self): self.returnPressed.emit()

    def checkListenWanted(self, widget, event): return True

    def eventFilter(self, widget, event):

        if self.listening and event.type()==QtCore.QEvent.KeyPress:

            c1=True 
            if self.listen_widget:
                if not widget in self.listen_widget: c1=False

            c2=True
            if self.exclude_widget:
                if widget in self.exclude_widget: c2=False

            if c1 and c2:

                if event.key() in  [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]: 

                    self.confirm()
                    event.accept()
                    return True
                        
                elif event.key()==QtCore.Qt.Key_Backspace:

                    self.clearKeys()
                    event.accept()
                    return True

                elif event.key()==QtCore.Qt.Key_Escape or event.text() == self.listen_leader:

                    if self.name!='normal':

                        self._onExecuteMatch()
                        event.accept()
                        return True

                else:

                    mode=self.checkMode(event)
                    event.accept()

                    if not mode:
                        self.addKeys(event)
                    else:
                        self._onExecuteMatch()
                        self.app.modes.setMode(mode.name)

                    return True

        elif event.type()==QtCore.QEvent.KeyPress:
            mode=self.checkMode(event)
            if mode:
                self.app.modes.setMode(mode.name)
                event.accept()
                return True

        return super().eventFilter(widget, event)

    def checkMode(self, event):

        for mode in self.app.modes.getModes():
            if mode.activateCheck(event): return mode

    def activateCheck(self, event):

        return event.text() == self.listen_leader

    def clearKeys(self):

        self.timer.stop()
        self.keys_pressed=[]
        self.app.main.bar.detail.clear()

    def delisten(self):

        self.clearKeys()
        if self.listening:
            self.listening=False
            if self.show_statusbar: self.app.main.bar.setData()

    def listen(self):

        self.listening=True

        self.clearKeys()
        self.app.main.bar.setData(self.data)

    def addKeys(self, event):

        self.timer.stop()
        if self.registerKey(event):
            key, digit = self.getKeys()
            self.keyPressed.emit(digit, key)
            matches, partial=self.getMatches(key, digit)
            self.reportMatches(matches, partial)
            self.runMatches(matches, partial, key, digit)

    def registerKey(self, event):
        
        # modifiers=QtWidgets.QApplication.keyboardModifiers()
        # if not text and moddies & Qt.ShiftModifier: 
        #     text='Shift'
        # if not text and moddies & Qt.ControlModifier: 
        #     text='Ctrl'
        
        text=event.text()
        if text: self.keys_pressed+=[text]
        return text

    def reportMatches(self, matches, partial):

        self.app.main.bar.detail.setText(
                f'{"".join(self.keys_pressed)}')

    def runMatches(self, matches, partial, key, digit):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(lambda: self.executeMatch(matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(0)
        else:
            if self.wait_time: self.timer.start(self.wait_time)

    def getKeys(self):

        key=''
        digit=''
        for i, k in enumerate(self.keys_pressed):
            if k.isnumeric():
                digit+=k
            else:
                key=''.join(self.keys_pressed[i:])
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None

        return key, digit

    def getMatches(self, key, digit):

        exact=[]
        partial=[]
        for data in self.commands:
            func=self._getFunc(data)
            k=data['down']
            if key==k[:len(key)]: 
                if digit:
                    if not 'digit' in inspect.signature(func).parameters: continue
                if key==k:
                    exact+=[data]
                elif key==k[:len(key)]: 
                    partial+=[data]
        return exact, partial

    def executeMatch(self, matches, partial, digit):

        if not partial:

            if not matches:
                self.clearKeys()
            elif len(matches)==1:
                self.clearKeys()
                if self.delisten_on_exec: self._onExecuteMatch()

                match=matches[0]['id']
                if digit and 'digit' in inspect.signature(match.func).parameters:
                    match(digit=digit)
                else:
                    match()

    def _getFunc(self, data): return data['id'].func

    def _onExecuteMatch(self):

        self.delistenWanted.emit(self.delisten_wanted)

    @register('q')
    def exit(self): self.app.exit()
