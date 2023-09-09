import re
from PyQt5 import QtCore
from inspect import signature

class EventListener(QtCore.QObject):

    tabPressed=QtCore.pyqtSignal()
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    backspacePressed=QtCore.pyqtSignal()
    carriageReturnPressed=QtCore.pyqtSignal()

    keysSet=QtCore.pyqtSignal(object)
    keysChanged=QtCore.pyqtSignal(str)
    keyPressed=QtCore.pyqtSignal(object, object)

    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    modeWanted=QtCore.pyqtSignal(object)
    listenWanted=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            app=None, 
            obj=None, 
            config={},
            leader='',
            special=[],
            wait_run=10,
            mode_keys={},
            wait_time=200,
            listen_leader=None, 
            command_leader=None,
            mode_on_exit='normal',
            delisten_on_exec=False,
            **kwargs,
            ):

        super().__init__(obj)

        self.obj=obj
        self.app=app
        self.methods={}
        self.commands={}
        self.config=config
        self.leader=leader
        self.pressed_text=''
        self.special=special
        self.keys_pressed=[]
        self.listening=False
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.mode_keys=mode_keys
        self.timer=QtCore.QTimer()
        self.mode_on_exit=mode_on_exit
        self.delisten_on_exec=delisten_on_exec

        self.listen_leader=self.parseKey(listen_leader)
        self.command_leader=self.parseKey(command_leader)
        self.setup()

    def setObj(self):

        if hasattr(self.obj, 'keyPressed'):
            self.keyPressed.connect(
                    self.obj.keyPressed)
        if hasattr(self.obj, 'tabPressed'):
            self.tabPressed.connect(
                    self.obj.tabPressed)
        if hasattr(self.obj, 'keysChanged'):
            self.keysChanged.connect(
                    self.obj.keysChanged)
        if hasattr(self.obj, 'returnPressed'):
            self.returnPressed.connect(
                    self.obj.returnPressed)
        if hasattr(self.obj, 'backspacePressed'):
            self.backspacePressed.connect(
                    self.obj.backspacePressed)
        if hasattr(self.obj, 'carriageReturnPressed'):
            self.carriageReturnPressed.connect(
                    self.obj.carriageReturnPressed)
        if hasattr(self.obj, 'forceDelisten'):
            self.forceDelisten.connect(
                    self.obj.forceDelisten)
        if hasattr(self.obj, 'delistenWanted'):
            self.delistenWanted.connect(
                    self.obj.delistenWanted)
        if hasattr(self.obj, 'modeWanted'):
            self.modeWanted.connect(
                    self.obj.modeWanted)
        if hasattr(self.obj, 'listenWanted'):
            self.listenWanted.connect(
                    self.obj.listenWanted)
        obj=self.obj
        if self.app: 
            obj=self.app
            plugman=getattr(self.app, 'plugman', None)
            if plugman:
                plugman.plugsLoaded.connect(
                        self.savePlugKeys)
        obj.installEventFilter(self)

    def setup(self):

        self.setObj()
        self.saveKeys()
        self.timer.timeout.connect(
                lambda: self.executeMatch([], [], 0))
        self.backspacePressed.connect(
                self.clearKeys)
        self.escapePressed.connect(
                self.on_escapePressed)

    def on_escapePressed(self): 

        if self.delisten_on_exec: 
            self.modeWanted.emit(self.mode_on_exit)
        else:
            self.delistenWanted.emit()
            if hasattr(self.obj, 'deactivate'):
                self.obj.deactivate()

    def clearKeys(self):

        self.timer.stop()
        self.pressed_text=''
        self.keys_pressed=[]

    def eventFilter(self, widget, event):

        if event.type()!=QtCore.QEvent.KeyPress:
            return False
        elif self.command_leader:
            if hasattr(self, 'commands'):
                c1=self.checkLeader(
                        event, 'command_leader')
                if c1:
                    self.obj.toggleCommandMode()
                    event.accept()
                    return True
        elif self.checkSpecialCharacters(event):
            event.accept()
            return True
        return self.addKeys(event)

    def addKeys(self, event):

        self.timer.stop()
        matches, partial = [], []
        if self.registerKey(event):
            key, digit = self.getKeys()
            self.keyPressed.emit(digit, key)
            matches, partial=self.getMatches(key, digit)
            self.runMatches(matches, partial, key, digit)
        if matches or partial: 
            return True
        else:
            self.clearKeys()
            return False

    def getPressed(self, event):

        text=[]
        pressed=[]
        mdf=event.modifiers()
        if (mdf & QtCore.Qt.AltModifier):
            pressed+=[QtCore.Qt.AltModifier]
            text+=['a']
        if (mdf & QtCore.Qt.ControlModifier):
            pressed+=[QtCore.Qt.ControlModifier]
            text+=['c']
        t=event.text()
        if t.isalpha():
            if (mdf & QtCore.Qt.ShiftModifier):
                pressed+=[QtCore.Qt.ShiftModifier]
        text+=[t]
        if t and t.isnumeric():
            pressed+=[t]
        else:
            pressed+=[event.key()]
        if len(text)>2:
            text='-'.join(text)
            text=f'<{text}>'
        else:
            text=''.join(text)
        return text, tuple(pressed)

    def registerKey(self, event):

        text, pressed=self.getPressed(event)
        if pressed and event.text():
            self.keys_pressed+=[pressed]
            self.pressed_text+=text
            self.keysChanged.emit(self.pressed_text)
        return pressed

    def getKeys(self):

        key, digit = [], ''
        for i, k in enumerate(self.keys_pressed):
            if type(k[0])==str:
                digit+=k[0]
            else:
                key=self.keys_pressed[i:]
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None
        return tuple(key), digit

    def getMatches(self, key, digit):

        m, p = [], []

        for v, f in self.commands.items():
            for (k, text) in v:
                if key==k[:len(key)]: 
                    if not digit is None:
                        t=getattr(f, '__wrapped__', f)
                        c1='digit' in signature(t).parameters
                        if not c1: continue
                    if key==k: 
                        m+=[f]
                    elif key==k[:len(key)]: 
                        p+=[f]
        return m, p

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

    def executeMatch(self, matches, partial, digit):

        if not partial:
            if len(matches)<2: 
                self.clearKeys()
            if len(matches)==1:
                self.on_executeMatch()
                m=matches[0]
                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters

                if digit and c1: 
                    m(digit=digit)
                else:
                    m()

    def on_executeMatch(self): 

        if self.delisten_on_exec: 
            self.keysChanged.emit('')
            self.modeWanted.emit(self.mode_on_exit)

    def saveKeys(self):

        for f in self.obj.__dir__():
            method=getattr(self.obj, f)
            if hasattr(method, 'key'):
                self.setKey(self.obj, method, method.name)

    def setKey(self, obj, method, name):

        self.methods[name]=method

        key=getattr(method, 'key')
        if key:
            mode_keys=getattr(obj, 'mode_keys', {})
            if hasattr(obj, 'event_listener'):
                mode_keys_l=getattr(
                        obj.event_listener, 'mode_keys', {})
                mode_keys.update(mode_keys_l)
            name=getattr(self.obj, 'name', None)
            prefix=mode_keys.get(name, '')
            match=self.parseKey(key, prefix=prefix)
            self.commands[match]=method

    def savePlugKeys(self):

        actions=self.app.plugman.actions
        for plug, actions in actions.items():
            for (pname, fname), m in actions.items():
                own_m=plug==self.obj
                any_m='any' in m.modes
                in_m=self.obj.name in m.modes
                if own_m or any_m or in_m:
                    self.setKey(plug, m, fname)
        self.keysSet.emit(self.commands)


    def parseKey(self, key, prefix=''):

        mapping={
                ',': 'Comma', 
                ';': 'Semicolon', 
                '.': 'Period',
                '-': 'Minus',
                '.': 'Period',
                '/': 'Slash',
                '+': 'Plus',
                '*': 'Asterisk',
                '@': 'At',
                '$': 'Dollar',
                '[': 'BracketLeft',
                ']': 'BracketRight',
                '_': 'Underscore',
                ' ': 'Space'
                }

        def parseLetter(t):

            unit=[]
            if t.isupper(): 
                unit+=[getattr(QtCore.Qt,'ShiftModifier')]
            k=mapping.get(t, t.upper())
            unit+=[getattr(QtCore.Qt, f"Key_{k}")]
            return unit

        def parse(key):

            parsed=[]
            p=r'(?P<group>(<[acAC]-.>)*)(?P<tail>([^<]*))'
            match=re.match(p, key)
            groups=match.group('group')
            if groups:
                groups=re.findall('<([^>]*)>', groups)
                for g in groups:
                    unit=[]
                    t=g.split('-', 1)
                    m, l = t[0], t[1]
                    if m in 'cC':
                        cm=getattr(QtCore.Qt,'ControlModifier')
                        unit+=[cm]
                    elif m in 'aA':
                        am=getattr(QtCore.Qt,'AltModifier')
                        unit+=[am]
                    unit+=parseLetter(l)
                    parsed+=[tuple(unit)]
            tails=match.group('tail')
            if tails:
                for t in list(tails):
                    unit=parseLetter(t)
                    parsed+=[tuple(unit)]
            return (tuple(parsed), key)

        parsed=[]
        if not key: return parsed 
        if type(key)==str: key=[key]
        for k in key: 
            k=f"{prefix}{k}"
            k=k.replace('<leader>', self.leader)
            parsed+=[parse(k)]
        return tuple(parsed)

    def checkLeader(self, event, kind='listen_leader'):

        text, pressed=self.getPressed(event)
        check_val=[]
        if kind=='listen_leader':
            if not self.listen_leader:
                return False
            for (v, k) in self.listen_leader:
                key=k
                check_val+=[v]
        elif kind=='command_leader':
            if not self.command_leader:
                return False
            for (v, k) in self.listen_leader:
                key=k
                check_val+=[v]
        if (pressed, ) in check_val: 
            self.keysChanged.emit(key)
            return True
        else:
            return False

    def checkSpecialCharacters(self, event):

        special=None
        enter=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]
        if event.key() in enter: 
            self.returnPressed.emit()
            special='return'
        elif event.key()==QtCore.Qt.Key_Backspace:
            self.backspacePressed.emit()
            special='backspace'
        elif event.key()==QtCore.Qt.Key_Escape:
            self.escapePressed.emit()
            special='escape'
        elif event.key()==QtCore.Qt.Key_Tab:
            self.tabPressed.emit()
            special='tab'
        elif event.modifiers()==QtCore.Qt.ControlModifier:
            if event.key()==QtCore.Qt.Key_BracketLeft:
                self.escapePressed.emit()
                special='escape_bracket'
            elif event.key()==QtCore.Qt.Key_M:
                self.carriageReturnPressed.emit()
                special='carriage'
        if special in self.special:
            return True
        else:
            return False
