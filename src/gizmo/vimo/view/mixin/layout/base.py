from PyQt5 import QtCore

from .utils import BaseLayout

class Layout:

    hasLayout=True
    layout_class=BaseLayout
    layoutChanged=QtCore.pyqtSignal(
            object, object)

    def setup(self):

        super().setup()
        self.setupLayout()

    def setupLayout(self):

        if self.layout_class:
            config=self.m_config.get(
                    'Layout', {})
            self.m_layout = self.layout_class(
                    self, config=config)

    def setLayout(self, layout):

        self.m_layout=layout
        self.layoutChanged.emit(
                self, self.m_layout)

    def prevItem(self, digit=1):

        idx=self.m_curr-digit+1 
        items=self.check('hasItems')
        pos=self.check('canPosition')
        if pos and items:
            c=self.m_layout.prev(
                    idx, self.count())
            self.goTo(c)
        
    def nextItem(self, digit=1): 

        idx=self.m_curr-digit+1 
        items=self.check('hasItems')
        pos=self.check('canPosition')
        if pos and items:
            c=self.m_layout.next(
                    idx, self.count())
            self.goTo(c)
