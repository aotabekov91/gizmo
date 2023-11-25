import re
from PyQt5 import QtCore

from gizmo.vimo.element import Element

class Model:

    kind=None
    name=None
    wantView=[]
    isType=False
    pattern=None
    wantUniqView=False
    element_class=Element
    loaded=QtCore.pyqtSignal()
    elementCreated=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            index=None,
            source=None,
            elements={},
            render=None,
            name=None,
            **kwargs,
            ):

        self.m_id=index
        self.m_data=None
        self.m_name=None
        self.m_loaded=False
        self.m_source=source
        self.m_render=render
        self.m_elements=elements
        self.kwargs=kwargs
        super().__init__()
        self.setup()

    def setup(self):

        self.setKind()
        self.setName()

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

    def elements(self):
        return self.m_elements

    def __eq__(self, o): 
        return o and id(self)==id(o)

    def __hash__(self): 
        return hash(self.m_data)

    def source(self): 
        return self.m_source

    def load(self):
        pass

    @classmethod
    def isCompatible(cls, source, **kwargs):

        if source and cls.pattern:
            p=cls.pattern
            return re.match(
                    p, source, re.I)

    @classmethod
    def getSourceName(cls, source, **kwargs):
        return source
