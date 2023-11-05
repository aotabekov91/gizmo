from PyQt5 import QtCore

from .utils import Runner
from ..base import Items

class PoolItems(Items):

    canPool=True
    modelLoaded=QtCore.pyqtSignal(
            object, object)

    def setup(self):

        super().setup()
        self.pool=QtCore.QThreadPool()

    def setItems(self):

        m=self.m_model
        self.m_items={}
        sf=self.scaleFactor
        c=self.m_config.get('Item', {})
        c=Runner(
                model=m,
                config=c,
                view=self,
                scaleFactor=sf,
                klass=self.item_class,
                )
        c.signals.created.connect(
                self.setupItem)
        c.signals.finished.connect(
                self.setupModel)
        self.pool.start(c)

    def setupModel(self):

        self.redraw()
        self.modelLoaded.emit(
                self, self.m_model)
