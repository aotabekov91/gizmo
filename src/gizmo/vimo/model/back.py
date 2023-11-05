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
            *args,
            index=None,
            source=None,
            elements={},
            **kwargs,
            ):

        self.m_id=index
        self.m_data=None
        self.m_loaded=False
        self.m_source=source
        self.m_elements=elements
        super().__init__()
        self.setup(*args, **kwargs)

    def count(self):
        return len(self.m_elements)

    def setup(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

    def assignId(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    def element(self, idx):
        return self.m_elements.get(idx, None)

    def elements(self):
        if not self.m_loaded:
            self.load()
        return self.m_elements

    def name(self):
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

    def sourceElement(self):
        pass

    @classmethod
    def isCompatible(cls, source):

        if source and cls.pattern:
            return re.match(
                    cls.pattern, 
                    source,
                    re.I)
