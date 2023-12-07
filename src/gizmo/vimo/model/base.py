import re
from PyQt5 import QtCore

from gizmo.vimo.element import Element

class Model:

    kind=None
    name=None
    wantView=[]
    isType=False
    pattern=None
    isLoaded=False
    wantUniqView=False
    element_class=Element
    loaded=QtCore.pyqtSignal(object)
    elementCreated=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            config={},
            name=None,
            index=None,
            source=None,
            elements={},
            render=None,
            **kwargs,
            ):

        self.m_id=index
        self.m_data=None
        self.m_name=name
        self.m_loaded=False
        self.m_source=source
        self.m_config=config
        self.m_render=render
        self.m_elements=elements.copy()
        self.kwargs=kwargs
        super().__init__()
        self.setup()

    def setup(self):

        self.setConf()
        self.setKind()
        self.setName()

    def setConf(self):

        c=self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setName(self):

        c=self.__class__.__name__
        c=self.m_name or c
        self.name=self.name or c

    def setKind(self):

        c=self.__class__.__name__
        self.kind=self.kind or c

    def render(self):
        return self.m_render

    def count(self):
        return len(self.m_elements)

    def readSuccess(self): 
        return self.m_data is not None

    def id(self): 
        return self.m_id

    def setId(self, idx): 
        self.m_id=idx

    def element(self, idx):
        return self.m_elements.get(idx, None)

    def elements(self):
        return self.m_elements

    def __eq__(self, o): 
        return o and id(self)==id(o)

    def __hash__(self): 
        return hash(self.m_data)

    def source(self): 
        return self.m_source

    def resetConfigure(self, **kwargs):
        pass

    def load(self):

        self.loaded.emit(self)
        self.isLoaded=True

    @classmethod
    def isCompatible(cls, s, **kwargs):

        if type(s)!=str: return
        if not cls.pattern: return
        return re.match(cls.pattern, s, re.I)

    @classmethod
    def getSourceName(cls, s, **kwargs):
        return s
