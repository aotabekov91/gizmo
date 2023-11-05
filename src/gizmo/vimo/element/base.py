class Element:

    def __init__(
            self, 
            data=None, 
            index=None, 
            model=None,
            ):

        self.m_id = index
        self.m_data = data
        self.m_model = model
        super().__init__()
        self.setup()
        self.load()

    def load(self):
        pass

    def size(self):
        pass

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
        return self.m_id

    def setIndex(self, idx):
        self.m_id=idx
