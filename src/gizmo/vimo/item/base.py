from PyQt5 import QtCore

class Item:

    def __init__(
            self, 
            config={},
            index=None,
            parent=None,
            element=None,
            **kwargs
            ):

        self.m_id=index
        self.m_config=config
        self.kwargs=kwargs
        self.setElement(element)
        super().__init__(parent)
        self.setup()

    def setup(self):
        pass

    def element(self):
        return self.m_element

    def setElement(self, element):
        self.m_element=element

    def index(self):
        return self.m_id

    def setIndex(self, idx):
        self.m_id=idx
