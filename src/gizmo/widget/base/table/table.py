from functools import partial
from PyQt5 import QtWidgets, QtCore

from .label import Label
from .line_edit import LineEdit
from .text_edit import TextEdit

class TableWidget(QtWidgets.QWidget):

    wmap={
        'Label': Label,
        'TextEdit':TextEdit,
        'LineEdit': LineEdit,
        }

    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            element, 
            item,
            wmap={},
            **kwargs):

        self.m_wmap=wmap
        self.m_item=item
        self.m_widgets={}
        self.m_element=element
        super().__init__(**kwargs)
        self.setup()

    def setup(self):
        
        self.m_layout=QtWidgets.QGridLayout(self)
        self.setLayout(self.m_layout)
        self.m_element.dataUpdated.connect(
                self.updateData)
        self.setData()

    def setData(self):

        items = self.m_wmap.items()
        for i, (n, d) in enumerate(items):
            w=d.get('w', 'Label')
            p=d.get('p', f'{i}x0x1x1')
            p=[int(f) for f in p.split('x')]
            w=self.wmap[w](
                    index=n,
                    parent=self, 
                    element=self.m_element,
                    )
            self.m_layout.addWidget(w, *p)
            self.m_widgets[n]=w
        self.updateData()

    def updateData(self):

        d=self.m_element.data()
        for n in self.m_widgets.keys():
            self.set(n, str(d[n]))

    def set(self, n, t):

        w = self.m_widgets[n]
        w.m_reporting=False
        w.setText(str(t))
        w.adjustSize()
        self.adjustSize()
        w.m_reporting=True

    def adjustSize(self):

        super().adjustSize()
        h=self.sizeHint()
        self.m_item.setSizeHint(h)
