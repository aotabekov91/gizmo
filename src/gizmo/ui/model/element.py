class Element:

    def __init__(
            self, 
            data=None, 
            item=None,
            index=None, 
            model=None,
            ):

        self.m_item = item
        self.m_data = data
        self.m_model = model
        self.m_index = index
        super().__init__()
        self.setup()

    def setup(self):
        pass

    def data(self): 
        return self.m_data

    def setData(self, data):
        self.m_data=data 

    def model(self): 
        return self.m_model

    def setModel(self, model):
        self.m_model=model

    def index(self): 
        return self.m_index

    def setIndex(self, idx):
        self.m_index=idx

    def item(self): 
        return self.m_item

    def setItem(self, item): 
        self.m_item=item
