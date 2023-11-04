import re
from inspect import signature
from PyQt5 import QtCore, QtWidgets

class Ear(QtCore.QObject):

    tabPressed=QtCore.pyqtSignal()
    keysSet=QtCore.pyqtSignal(
            object)
    keysChanged=QtCore.pyqtSignal(
            str)
    keyRegistered=QtCore.pyqtSignal(
            object)
    keyPressed=QtCore.pyqtSignal(
            object, object)
    modeWanted=QtCore.pyqtSignal(
            object)
    listenWanted=QtCore.pyqtSignal(
            object)
    earingStarted=QtCore.pyqtSignal(
            object)
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    backspacePressed=QtCore.pyqtSignal()
    escapeBracketPressed=QtCore.pyqtSignal()
    carriageReturnPressed=QtCore.pyqtSignal()

    def __init__(
            self, 
            app=None, 
            obj=None, 
            config={},
            special=[],
            wait_run=40,
            wait_time=200,
            leader_keys={},
            listening=False,
            report_keys=True,
            listen_leader=None, 
            suffix_functor=None,
            mode_on_exit='normal',
            delisten_on_exec=False,
            delisten_keys=['escape', 'escape_bracket'],
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
        self.report_keys=report_keys
        self.leader_keys=leader_keys
        self.mode_on_exit=mode_on_exit
        self.delisten_keys=delisten_keys
        self.suffix_functor=suffix_functor
        self.delisten_on_exec=delisten_on_exec
        self.listen_leader=self.parseKey(
                listen_leader)
        self.setup()

    def listen(self):

        self.clearKeys()
        self.listening=True
        self.earingStarted.emit(self)
        qapp=QtWidgets.QApplication.instance()
        if qapp:
            qapp.earGained.emit(self)

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
            self.app.moder.plugsLoaded.connect(
                    self.savePlugKeys)
            obj=self.app.uiman.qapp
        else:
            self.saveOwnKeys()
        obj.installEventFilter(self)

    def toggleMode(self, mode):
        mode.toggle()

    def setup(self):

        self.setObj()
        self.timer=QtCore.QTimer()
        f=lambda: self.executeMatch([], [], 0)
        self.timer.timeout.connect(f)
        self.backspacePressed.connect(
                self.clearKeys)
        self.escapePressed.connect(
                self.on_escapePressed)
        self.setKeyMap()
        qapp=QtWidgets.QApplication.instance()
        if qapp:
            qapp.earSet.emit(self)

    def setKeyMap(self):

        self.key_map={}
        for n, v in vars(QtCore.Qt).items():
            c1 = n.startswith('Key_')
            c2 = n.endswith('Modifier')
            if c1 or c2: 
                if c1: 
                    n=n.replace('Key_', '').lower()
                self.key_map[v]=n

    def on_escapePressed(self): 

        self.clearKeys()
        if self.delisten_on_exec: 
            self.modeWanted.emit(
                    self.mode_on_exit)
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
            if self.report_keys:
                self.keysChanged.emit(
                        self.pressed_text)
        self.keyRegistered.emit(event)

    # def eventFilter(
    #         self, 
    #         widget, 
    #         event
    #         ):
    #     # if not self.listening:
    #     #     return False
    #     # if event.type()!=QtCore.QEvent.KeyPress:
    #     #     return False
    #     # m, p  = self.checkSpecial(event)
    #     # if m:
    #     #     event.accept()
    #     #     return True
    #     # self.registerKey(event)
    #     # if self.checkLeader(event):
    #     #     event.accept()
    #     #     return True
    #     # elif p in self.delisten_keys:
    #     #     self.escapePressed.emit()
    #     #     event.accept()
    #     #     return True
    #     # return self.addKeys(event)

    # def addKeys(self, event):
        # self.timer.stop()
        # matches, partial = [], []
        # if self.pressed:
        #     key, digit = self.getKeys()
        #     matches, partial=self.getMatches(
        #             key, digit)
        #     self.runMatches(
        #             matches, 
        #             partial, 
        #             key, 
        #             digit)
        # if matches or partial: 
        #     return True
        # # elif self.suffix_functor:
        #     # return self.suffix_functor(
        #             # key, digit, event)
        # else:
        #     self.clearKeys()
        #     return False

    def eventFilter(
            self, 
            widget, 
            event
            ):

        if not self.listening:
            return False
        if event.type()!=QtCore.QEvent.KeyPress:
            return False
        m, p  = self.checkSpecial(event)
        if m:
            event.accept()
            return True
        self.registerKey(event)
        if self.checkLeader(event):
            event.accept()
            return True
        elif p in self.delisten_keys:
            self.escapePressed.emit()
            event.accept()
            return True
        elif self.addKeys(event):
            event.accept()
            return True
        elif self.suffix_functor:
            return self.suffix_functor(event)
        else:
            self.clearKeys()
            return False

    def addKeys(self, event):

        self.timer.stop()
        m, p = [], []
        if self.pressed:
            k, d = self.getKeys()
            m, p=self.getMatches(k, d)
            self.runMatches(m, p, k, d)
        return m or p

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
                if shift: 
                    n=n.upper()
                p+=[n]
        if len(p)==1:
            return p[0]
        return f'<{"-".join(p)}>'
        

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

    def runMatches(
            self, 
            matches, 
            partial, 
            key, 
            digit
            ):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(
                lambda: self.executeMatch(
                    matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(self.wait_run)
        else:
            if self.wait_time: 
                self.timer.start(self.wait_time)

    def executeMatch(
            self, 
            matches, 
            partial, 
            digit
            ):

        if not partial:
            if len(matches)<2: 
                self.clearKeys()
            if len(matches)==1:
                self.on_executeMatch()
                m=matches[0]
                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters
                if digit is not None and c1: 
                    m(digit=digit)
                else:
                    m()

    def on_executeMatch(self): 

        if self.delisten_on_exec: 
            self.keysChanged.emit('')
            self.modeWanted.emit(
                    self.mode_on_exit)

    def setKey(self, obj, method, name):

        self.methods[name]=method
        key=getattr(method, 'key')
        if key:
            oname=getattr(
                    self.obj, 'name', None)
            leader_keys=getattr(
                    obj, 'leader_keys', {})
            ear=getattr(obj, 'ear', None)
            if ear: 
                leader_keys.update(ear.leader_keys)
            prefix=leader_keys.get(oname, '')
            match=self.parseKey(key, prefix=prefix)
            self.matches[name]=match
            self.commands[match]=method

    def saveOwnKeys(self):

        for f in self.obj.__dir__():
            mode=getattr(self.obj, f)
            if hasattr(mode, 'key'):
                own_m=len(mode.modes)==0
                in_m=self.obj.name in mode.modes
                if any([own_m, in_m]):
                    self.setKey(
                            self.obj, 
                            mode, 
                            mode.name)

    def savePlugKeys(self):

        actions=self.app.moder.actions
        for obj, col in actions.items():
            for (pn, fn), m in col.items():
                any_='any' in m.modes
                own=obj==self.obj
                own=own and len(m.modes)==0
                in_=self.obj.name in m.modes
                if any([own, any_, in_]):
                    self.setKey(obj, m, fn)
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
            ms=self.app.moder.plugs.items()
            for _, m in ms:
                f=getattr(m, 'checkLeader', None)
                if f and f(event, pressed):
                    self.timer.stop()
                    self.timer.timeout.disconnect()
                    func=lambda: self.toggleMode(m)
                    self.timer.timeout.connect(func)
                    self.timer.start(self.wait_run)
                    return True

    def checkSpecial(self, event):

        m, p = False, None
        e=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]
        if event.key() in e: 
            p='return'
            if p in self.special:
                m=True
                self.returnPressed.emit()
        elif event.key()==QtCore.Qt.Key_Backspace:
            p='backspace'
            if p in self.special:
                m=True
                self.backspacePressed.emit()
        elif event.key()==QtCore.Qt.Key_Escape:
            p='escape'
            if p in self.special:
                m=True
                self.escapePressed.emit()
        elif event.key()==QtCore.Qt.Key_Tab:
            p='tab'
            if p in self.special:
                m=True
                self.tabPressed.emit()
        elif event.modifiers()==QtCore.Qt.ControlModifier:
            if event.key()==QtCore.Qt.Key_BracketLeft:
                p='escape_bracket'
                if p in self.special:
                    m=True
                    self.escapeBracketPressed.emit()
            elif event.key()==QtCore.Qt.Key_M:
                p='carriage'
                if p in self.special:
                    m=True
                    self.carriageReturnPressed.emit()
        if m: 
            self.clearKeys()
        return m, p
