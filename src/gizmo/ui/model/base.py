class Model:

    def __init__(
            self, 
            data=None,
            elements={},
            source=None,
            ):

        self.m_data=data
        self.m_source=source
        self.m_elements=elements
        super().__init__()
        self.load(source)

    def load(self, source):
        pass

    def id(self): 
        return self.m_id

    def setId(self, idx): 
        self.m_id=idx

    def source(self): 
        return self.m_source

    def readSuccess(self): 
        return self.m_data is not None

    def element(self, idx): 
        return self.m_elements.get(idx, None)

    def elements(self): 
        return self.m_elements

    def setElements(self, data):
        pass

    def save(self, *args, **kwargs):
        pass

    def name(self):
        pass

    def count(self):
        return len(self.elements())

    def __eq__(self, other): 
        return self.m_data==other.m_data

    def __hash__(self): 
        return hash(self.m_data)
