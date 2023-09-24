import re
from PyQt5 import QtCore
from inspect import signature

class Ear(QtCore.QObject):

    tabPressed=QtCore.pyqtSignal()
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    backspacePressed=QtCore.pyqtSignal()
    carriageReturnPressed=QtCore.pyqtSignal()

    keysSet=QtCore.pyqtSignal(object)
    keysChanged=QtCore.pyqtSignal(str)
    keyRegistered=QtCore.pyqtSignal(object)
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
            special=[],
            wait_run=40,
            prefix_keys={},
            wait_time=200,
            listening=False,
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
        self.matches={}
        self.commands={}
        self.pressed=None
        self.config=config
        self.pressed_text=''
        self.special=special
        self.pressed_keys=[]
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.listening=listening
        self.prefix_keys=prefix_keys
        self.mode_on_exit=mode_on_exit
        self.delisten_on_exec=delisten_on_exec

        self.listen_leader=self.parseKey(listen_leader)
        self.command_leader=self.parseKey(command_leader)
        self.setup()

    def listen(self):

        self.listening=True
        self.clearKeys()

    def delisten(self):

        self.listening=False
        self.timer.stop()
        self.clearKeys()

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
        self.setActions()

    def setActions(self):

        obj=self.obj
        if self.app: 
            self.app.plugman.plugsLoaded.connect(
                    self.savePlugKeys)
            obj=self.app.uiman.qapp
        else:
            self.saveOwnKeys()
        obj.installEventFilter(self)

    def toggleMode(self, mode):

        if mode==self.obj:
            self.delistenWanted.emit()
        else:
            self.modeWanted.emit(mode)

    def setup(self):

        self.setObj()
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                lambda: self.executeMatch([], [], 0))
        self.backspacePressed.connect(
                self.clearKeys)
        self.escapePressed.connect(
                self.on_escapePressed)
        self.setKeyMap()

    def setKeyMap(self):

        self.key_map={}
        for n, v in vars(QtCore.Qt).items():
            c1 = n.startswith('Key_')
            c2 = n.endswith('Modifier')
            if c1 or c2: 
                if c1: n=n.replace('Key_', '').lower()
                self.key_map[v]=n

    def on_escapePressed(self): 

        if self.delisten_on_exec: 
            self.modeWanted.emit(self.mode_on_exit)
        else:
            self.delistenWanted.emit()
            if hasattr(self.obj, 'deactivate'):
                self.obj.deactivate()

    def clearKeys(self):

        self.timer.stop()
        self.pressed=None
        self.pressed_text=''
        self.pressed_keys=[]

    def registerKey(self, event):

        self.pressed=self.getPressed(event)
        if self.pressed and event.text():
            text=self.getText(self.pressed)
            self.pressed_text+=text
            self.pressed_keys+=[self.pressed]
            self.keysChanged.emit(self.pressed_text)
        self.keyRegistered.emit(event)

    def eventFilter(self, widget, event):

        if not self.listening:
            return False
        if event.type()!=QtCore.QEvent.KeyPress:
            return False
        self.registerKey(event)
        if self.checkLeader(event):
            event.accept()
            return True
        elif self.checkSpecialCharacters(event):
            event.accept()
            return True
        return self.addKeys(event)

    def addKeys(self, event):

        self.timer.stop()
        matches, partial = [], []
        if self.pressed:
            key, digit = self.getKeys()
            matches, partial=self.getMatches(key, digit)
            self.runMatches(matches, partial, key, digit)

        if matches or partial: 
            return True
        else:
            self.clearKeys()
            return False

    def getPressed(self, event):

        pressed = []
        mdf=event.modifiers()
        if (mdf & QtCore.Qt.AltModifier):
            pressed+=[QtCore.Qt.AltModifier]
        if (mdf & QtCore.Qt.ControlModifier):
            pressed+=[QtCore.Qt.ControlModifier]
        if (mdf & QtCore.Qt.ShiftModifier):
            if event.text().isalpha():
                pressed+=[QtCore.Qt.ShiftModifier]
            elif QtCore.Qt.ControlModifier in pressed:
                pressed+=[QtCore.Qt.ShiftModifier]
        pressed+=[event.key()]
        return tuple(pressed)

    def getText(self, pressed):

        p=[]
        shift=False
        for i in pressed:
            n=self.key_map[i]
            if n == 'ControlModifier':
                p+=['c']
            elif n == 'ShiftModifier':
                shift=True
            else:
                if shift: n=n.upper()
                p+=[n]
        return '-'.join(p)

    def getKeys(self):


        key, digit = [], ''
        for i, k in enumerate(self.pressed_keys):
            p=self.key_map[k[0]]
            if p.isnumeric():
                digit+=p
            else:
                key=self.pressed_keys[i:]
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None
        return tuple(key), digit

    def getMatches(self, key, digit):

        m, p = [], []
        for v, f in self.commands.items():
            for k in v:
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

    def setKey(self, obj, method, name):

        self.methods[name]=method
        key=getattr(method, 'key')
        if key:
            prefix_keys=getattr(obj, 'prefix_keys', {})
            ear=getattr(obj, 'ear', None)
            if ear: 
                prefix_keys.update(ear.prefix_keys)
            oname=getattr(self.obj, 'name', None)
            prefix=prefix_keys.get(oname, '')
            match=self.parseKey(key, prefix=prefix)
            self.matches[name]=match
            self.commands[match]=method

    def saveOwnKeys(self):

        for f in self.obj.__dir__():
            m=getattr(self.obj, f)
            if hasattr(m, 'key'):
                own_m=len(m.modes)==0
                in_m=self.obj.name in m.modes
                if any([own_m, in_m]):
                    self.setKey(self.obj, m, m.name)

    def savePlugKeys(self):

        actions=self.app.plugman.actions
        for obj, actions in actions.items():
            for (pname, fname), m in actions.items():
                any_='any' in m.modes
                own=obj==self.obj
                own=own and len(m.modes)==0
                in_=self.obj.name in m.modes
                if any([own, any_, in_]):
                    self.setKey(obj, m, fname)
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
            return tuple(parsed) 

        parsed=[]
        if not key: 
            return () 
        if type(key)==str: 
            key=[key]
        for k in key: 
            parsed+=[parse(f"{prefix}{k}")]
        return tuple(parsed)

    def checkLeader(self, event):

        pressed=(self.pressed,)

        if self.app:
            ms=self.app.plugman.plugs.items()
            for _, m in ms:
                f=getattr(m, 'checkLeader', None)
                if f and f(event, pressed):
                    self.timer.stop()
                    self.timer.timeout.disconnect()
                    func=lambda: self.toggleMode(m)
                    self.timer.timeout.connect(func)
                    self.timer.start(self.wait_run)
                    return True
        else:
            if pressed in self.command_leader:
                self.obj.toggleCommandMode()
                return True

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