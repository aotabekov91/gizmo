from PyQt5 import QtCore

from gizmo.vimo.element import Element

class Model:

    element_class=Element
    loaded=QtCore.pyqtSignal()
    elementCreated=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            kind=None,
            index=None,
            source=None,
            elements={},
            render=None,
            **kwargs,
            ):

        self.m_id=index
        self.m_data=None
        self.m_kind=kind
        self.m_loaded=False
        self.m_source=source
        self.m_render=render
        self.m_elements=elements
        self.kwargs=kwargs
        super().__init__()
        self.setup()

    def kind(self):
        return self.m_kind

    def render(self):
        return self.m_render

    def count(self):
        return len(self.m_elements)

    def setup(self):
        pass

    def readSuccess(self): 
        return self.m_data is not None

    def id(self): 
        return self.m_id

    def setId(self, idx): 
        self.m_id=idx

    def elements(self):
        return self.m_elements

    def __eq__(self, o): 
        return o and self.m_data==o.m_data

    def __hash__(self): 
        return hash(self.m_data)

    def source(self): 
        return self.m_source
