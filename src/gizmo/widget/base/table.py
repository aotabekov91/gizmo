from functools import partial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel as Label
from PyQt5.QtWidgets import QTextEdit as TextEdit

class TableWidget(QtWidgets.QWidget):

    wmap={
        'Label': Label,
        'TextEdit':TextEdit
        }

    widgetDataChanged=QtCore.pyqtSignal(
            object, object)

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
            w=self.wmap[w](parent=self)
            self.m_layout.addWidget(w, *p)
            s=getattr(w, 'widgetTextChanged', None)
            if s: s.connect(self.widgetDataChanged)
            self.m_widgets[n]=(w, s)
        self.updateData()

    def updateData(self):

        data=self.m_element.data()
        for n in self.m_widgets.keys():
            self.set(n, str(data[n]))

    def set(self, n, t):

        w, s = self.m_widgets[n]
        if s: s.disconnect(self.widgetDataChanged)
        w.setText(str(t))
        w.adjustSize()
        self.adjustSize()
        if s: s.connect(self.widgetDataChanged)

    def adjustSize(self):

        super().adjustSize()
        h=self.sizeHint()
        self.m_item.setSizeHint(h)
