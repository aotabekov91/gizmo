from PyQt5 import QtCore 
from inspect import signature

from ...plug import PlugObj
from ...utils import register

class Mode(PlugObj):

    def __init__(self, 
                 wait_run=2,
                 wait_time=100,
                 report_keys=True,
                 delisten_on_exec=True,
                 **kwargs):

        self.commands={}
        self.keys_pressed=[]
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.report_keys=report_keys

        self.delisten_on_exec=delisten_on_exec

        super(Mode, self).__init__(
                command_leader=[], 
                **kwargs)

    def setup(self):

        super().setup()
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.deactivate)

    def setPlugData(self):

        def setData(plug, actions, mname=None):

            for (pname, fname), m in actions.items():
                if not mname or  mname in m.modes:
                    if hasattr(m, 'key'): 
                        prefix=plug.modeKey(self.name)
                        key=f'{prefix}{m.key}'
                        self.commands[key]=m

        for plug, actions in self.app.manager.actions.items():
            setData(plug, actions, self.name)

        own_actions=self.app.manager.actions.get(self)
        if own_actions: setData(self, own_actions)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.KeyPress
        if self.listening and c1: 

            enter=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]

            if event.key() in enter: 

                self.returnPressed.emit()
                event.accept()
                return True
                    
            elif event.key()==QtCore.Qt.Key_Backspace:

                self.clearKeys()
                event.accept()
                return True

            elif event.key()==QtCore.Qt.Key_Escape:

                self._onExecuteMatch()
                event.accept()
                return True

            elif event.key()==QtCore.Qt.Key_BracketLeft:

                if event.modifiers()==QtCore.Qt.ControlModifier:

                    self._onExecuteMatch()
                    event.accept()
                    return True

            else:

                mode=self.checkListen(event)
                if not mode:
                    self.addKeys(event)
                    event.accept()
                    return True

        return super().eventFilter(widget, event)

    def clearKeys(self):

        self.timer.stop()
        self.keys_pressed=[]

    def listen(self):

        super().listen()
        self.clearKeys()

    def delisten(self):

        super().delisten()
        self.timer.stop()
        self.clearKeys()

    def addKeys(self, event):

        self.timer.stop()
        if self.registerKey(event):
            key, digit = self.getKeys()
            self.keyPressed.emit(digit, key)
            matches, partial=self.getMatches(key, digit)
            self.runMatches(matches, partial, key, digit)

    def registerKey(self, event):
        
        text=event.text()
        if text: self.keys_pressed+=[text]
        return text

    def runMatches(self, matches, partial, key, digit):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(
                lambda: self.executeMatch(
                    matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(self.wait_run)
        else:
            if self.wait_time: 
                self.timer.start(self.wait_time)

    def getKeys(self):

        key, digit = '', ''

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

        m, p = [], []

        for k, f in self.commands.items():
            if key==k[:len(key)]: 
                if digit:
                    t=getattr(f, '__wrapped__', f)
                    c1='digit' in signature(t).parameters
                    if not c1: continue
                if key==k: 
                    m+=[f]
                elif key==k[:len(key)]: 
                    p+=[f]
        return m, p

    def executeMatch(self, matches, partial, digit):

        if not partial:

            if len(matches)<2: 
                self.clearKeys()

            if len(matches)==1:
                if self.delisten_on_exec: self._onExecuteMatch()

                m=matches[0]

                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters

                if digit and c1: 
                    m(digit=digit)
                else:
                    m()

    def _onExecuteMatch(self): self.delistenWanted.emit()

    @register('q')
    def exit(self): self.app.exit()
