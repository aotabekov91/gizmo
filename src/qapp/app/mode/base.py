import inspect

from PyQt5 import QtCore 

from ..plug import Plug
from ...utils import register
from ...widget import ListWidget 

class Mode(Plug):

    returnPressed=QtCore.pyqtSignal()
    listenWanted=QtCore.pyqtSignal(str)
    delistenWanted=QtCore.pyqtSignal(str)

    def __init__(self, 
                 wait_time=250,
                 listening=False,
                 listen_leader=None,
                 show_commands=False,
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

        self.show_commands=show_commands
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

        self.commands=sorted(self.commands, key=lambda x: x['plug'])
        self.ui.mode.setList(self.commands)

    def setPlugData(self, plug, actions, mode_name=None):

        for (plug_name, func_name), method in actions.items():
            if not mode_name or  mode_name in method.modes:
            # if not mode_name or plug_name==self.name or  mode_name in method.modes:
                method_name=getattr(method, 'info', None)
                if method_name: func_name=method_name
                name=f'[{plug_name}] {func_name}'
                data={'id': method, 'up': name, 'plug': plug_name}
                if method.key: 
                    key=method.key
                    if hasattr(plug, 'modeKey'): 
                        prefix=plug.modeKey(self.name)
                        key=f'{prefix}{key}'
                    data['down']=key
                self.commands+=[data]

    def setUI(self):
        
        super().setUI()

        mode=ListWidget(exact_match=True, check_fields=['down'])
        self.ui.addWidget(mode, 'mode')

        self.ui.mode.returnPressed.connect(self.confirm)
        self.ui.mode.hideWanted.connect(self.deactivate)
        self.ui.focusGained.connect(self.activate)
        self.ui.installEventFilter(self)

    def activate(self):

        self.app.modes.delisten()
        self.app.main.bar.setData(self.data)
        self.listening=True

    def confirm(self):
        
        self.returnPressed.emit()

        if self.ui.mode.isVisible():

            item=self.ui.mode.item(self.ui.mode.currentRow())
            if item:
                matches=[item.itemData]
                self.reportMatches(matches, [])
                self.runMatches(matches, [], None, None)

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

                if event.modifiers() and self.ui.isVisible():

                    if event.key() in [QtCore.Qt.Key_N, QtCore.Qt.Key_J]:
                        self.ui.mode.move(crement=1)
                        event.accept()
                        return True

                    elif event.key() in [QtCore.Qt.Key_P, QtCore.Qt.Key_K]:
                        self.ui.mode.move(crement=-1)
                        event.accept()
                        return True

                    elif event.key() in  [QtCore.Qt.Key_M, QtCore.Qt.Key_L]: 
                        self.confirm()
                        event.accept()
                        return True
                        
                    elif event.key() in  [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]: 
                        self.confirm()
                        event.accept()
                        return True

                elif event.key() in  [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]: 

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

                    if not mode:

                        self.addKeys(event)
                        event.accept()
                        return True

                    else:

                        self.app.modes.setMode(mode.name)
                        self._onExecuteMatch()
                        event.accept()
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
        self.ui.mode.unfilter()

    def delisten(self):

        self.clearKeys()
        if self.listening:
            self.listening=False
            if self.ui.activated: self.ui.deactivate()
            if self.show_statusbar: self.app.main.bar.setData()

    def listen(self):

        self.listening=True

        self.clearKeys()
        self.app.main.bar.setData(self.data)

        if self.show_commands: 
            self.ui.activate()
            self.ui.show(self.ui.mode)

    def addKeys(self, event):

        self.timer.stop()
        if self.registerKey(event):
            key, digit = self.getKeys()
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

        if self.ui.isVisible(): self.ui.mode.setFilterList(matches+partial)
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

    def toggleCommands(self):

        if self.ui.mode.isVisible():
            self.ui.deactivate()
        else:
            self.ui.activate()
            self.ui.show(self.ui.mode)

    @register('q')
    def exit(self): self.app.exit()
