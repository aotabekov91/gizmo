class Item:

    def __init__(
            self, 
            config={},
            size=None,
            index=None,
            parent=None,
            element=None,
            **kwargs
            ):

        self.m_id=index
        self.m_size=size
        self.m_config=config
        self.m_element = element
        self.kwargs=kwargs
        super().__init__(parent)
        self.setup()

    def setup(self):
        pass

    def size(self):
        return self.m_size

    def element(self):
        return self.m_element

    def setElement(self, element):
        self.m_element=element

    def index(self):
        return self.m_id

    def setIndex(self, idx):
        self.m_id=idx

    def checkProp(self, prop):
        return hasattr(self, prop) 
