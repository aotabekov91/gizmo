import re
from PyQt5 import QtCore

from gizmo.vimo.element import Element

class Model:

    kind=None
    pattern=None
    element_class=Element
    loaded=QtCore.pyqtSignal()
    elementCreated=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            index=None,
            source=None,
            elements={},
            render=None,
            **kwargs,
            ):

        self.m_id=index
        self.m_data=None
        self.m_loaded=False
        self.m_source=source
        self.m_render=render
        self.m_elements=elements
        self.kwargs=kwargs
        super().__init__()
        self.setup()

    def render(self):
        return self.m_render

    def setup(self):
        pass

    def readSuccess(self): 
        return self.m_data is not None

    def id(self): 
        return self.m_id

    def setId(self, idx): 
        self.m_id=idx

    def __eq__(self, other): 
        return self.m_data==other.m_data

    def __hash__(self): 
        return hash(self.m_data)

    def source(self): 
        return self.m_source

    @classmethod
    def isCompatible(cls, source):

        if source and cls.pattern:
            return re.match(
                    cls.pattern, 
                    source,
                    re.I)
