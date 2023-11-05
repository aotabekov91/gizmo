class Annotation:

    def __init__(
            self, data=None):

        self.m_data = data
        super().__init__()

    def setId(self, idx): 
        self.m_id=idx

    def id(self): 
        return self.m_id

    def element(self): 
        return self.m_element
    
    def setElement(self, page): 
        self.m_element=page

    def data(self): 
        return self.m_data

    def setData(self, data): 
        self.m_data=data
