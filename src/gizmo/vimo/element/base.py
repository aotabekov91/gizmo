from PyQt5 import QtGui, QtCore

class Element(QtCore.QObject):

    dataSet=QtCore.pyqtSignal()
    dataUpdated=QtCore.pyqtSignal()
    dataChanged=QtCore.pyqtSignal()

    def __init__(
            self, 
            data=None, 
            index=None, 
            model=None,
            ):

        self.m_id = index
        self.m_model = model
        self.m_norm= QtGui.QTransform()
        super().__init__()
        self.setData(data)
        self.setup()
        self.load()
        self.updateTrans()

    def data(self, field=None): 

        if field:
            return self.m_data.get(field, None)
        return self.m_data

    def setData(self, data):
        
        self.m_data=data
        self.dataSet.emit()

    def updateData(self, data):

        self.m_data.update(data)
        self.dataUpdated.emit()

    def updateTrans(self):

        n=self.m_norm
        s=self.size()
        n.scale(s.width(), s.height())
        ninv=n.inverted()[0]
        self.m_norm_inv=ninv

    def size(self):
        return QtCore.QSize(0, 0)

    def load(self):
        pass

    def setup(self):
        pass

    def model(self): 
        return self.m_model

    def setModel(self, model):
        self.m_model=model

    def index(self): 
        return self.m_id

    def setIndex(self, idx):
        self.m_id=idx
