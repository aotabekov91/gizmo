from PyQt5 import QtCore

class View:

    position=None
    hasRender=True
    modelChanged=QtCore.pyqtSignal(
            object, object)
    modelIsToBeChanged=QtCore.pyqtSignal(
            object, object)

    def __init__(
            self, 
            app=None, 
            config={},
            name=None,
            model=None,
            index=None,
            parent=None,
            render=None,
            objectName='View',
            **kwargs,
            ):

        self.app=app
        self.m_id=index
        self.m_name=name
        self.m_model = model
        self.m_config=config
        self.m_render=render
        super().__init__(
                parent=parent,
                objectName=objectName)
        self.setup()

    def name(self):
        if self.m_name:
            return self.m_name
        return self.__class__.__name__

    def render(self):
        return self.m_render

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

    def __bool__(self):
        return True
