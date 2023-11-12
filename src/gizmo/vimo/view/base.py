from PyQt5 import QtCore

class View:

    position=None
    modelChanged=QtCore.pyqtSignal(
            object, object)
    modelIsToBeChanged=QtCore.pyqtSignal(
            object, object)

    def __init__(
            self, 
            app=None, 
            config={},
            model=None,
            index=None,
            parent=None,
            objectName='View',
            **kwargs,
            ):

        self.app=app
        self.m_id=index
        self.m_model = model
        self.m_config=config
        super().__init__(parent=parent)
        self.setup()

    def setSettings(self):

        c=self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setup(self):

        self.setSettings()
        self.setupScrollBars()

    def setId(self, vid):
        self.m_id=vid

    def id(self):
        return self.m_id

    def model(self): 
        return self.m_model

    def setModel(self, model):

        self.modelIsToBeChanged.emit(
                self, self.m_model)
        self.m_model=model
        self.modelChanged.emit(
                self, model)

    def setupScrollBars(self):

        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

    def name(self):

        if self.m_model:
            return self.m_model.id()

    def check(self, what, v=None):

        v=v or self
        if type(what)!=list:
            what=[what]
        for w in what:
            if not getattr(v, w, False):
                return False
        return True

    def cleanUp(self):
        pass
