from PyQt5 import QtCore

class View:

    name=None
    kind=None
    position={}
    activated=False
    focusLost=QtCore.pyqtSignal(
            object)
    focusGained=QtCore.pyqtSignal(
            object)
    modelChanged=QtCore.pyqtSignal(
            object, object)
    activateWanted=QtCore.pyqtSignal(
            object)
    octivateWanted=QtCore.pyqtSignal(
            object)
    modelIsToBeChanged=QtCore.pyqtSignal(
            object, object)

    def __init__(
            self, 
            app=None, 
            config={},
            name=None,
            model=None,
            index=None,
            parent=None,
            objectName='View',
            **kwargs,
            ):

        self.app=app
        self.m_id=index
        self.m_name=name
        self.m_model = model
        self.m_config=config
        super().__init__(
                parent=parent,
                objectName=objectName)
        self.setup()

    def setup(self):

        self.setConf()
        self.setName()
        self.setBars()

    def setName(self):

        c=self.__class__.__name__
        c=self.m_name or c
        self.name=self.name or c

    def setConf(self):

        c=self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setId(self, vid):
        self.m_id=vid

    def id(self):
        return self.m_id

    def model(self): 
        return self.m_model

    def setModel(self, model):

        if self.m_model!=model:
            self.modelIsToBeChanged.emit(
                    self, self.m_model)
            self.m_model=model
            self.kind=model.kind
            self.modelChanged.emit(
                    self, model)

    def setBars(self):

        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

    def check(self, what, v=None):

        v=v or self
        if type(what)!=list:
            what=[what]
        for w in what:
            if not getattr(v, w, False):
                return False
        return True

    def cleanUp(self):
        pass

    def toggle(self):

        if self.activated: 
            self.octivate()
        else:
            self.activate()

    def octivate(self):

        self.activated=False
        self.octivateWanted.emit(self)

    def activate(self):

        self.activated=True
        self.activateWanted.emit(self)

    def __bool__(self):
        return True

    def resetConfigure(self, **kwargs):
        pass

    @classmethod
    def isCompatible(cls, m, **kwargs):

        n=cls.name or cls.__name__
        return n in getattr(m, 'wantView', [])

    def setFocus(self):

        super().setFocus()
        self.focusGained.emit(self)
