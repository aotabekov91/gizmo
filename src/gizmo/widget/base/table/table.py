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

        self.m_map=wmap
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

        for n, d in self.m_map.items():
            w, p = d['w'], d['p']
            p=[int(f) for f in p.split('x')]
            w=self.wmap[w](parent=self, index=n)
            self.m_layout.addWidget(w, *p)
            s=getattr(w, 'widgetDataChanged', None)
            if s: s.connect(self.on_widgetDataChanged)
            self.m_widgets[n]=w
        self.updateData()

    def on_widgetDataChanged(self, cdict):

        d=self.m_element.data()
        d.update(cdict)
        self.widgetDataChanged.emit(
                self.m_element)

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
