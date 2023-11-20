from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel as Label
from PyQt5.QtWidgets import QTextEdit as TextEdit

class TableWidget(QtWidgets.QWidget):

    wmap={
        'Label': Label,
        'TextEdit':TextEdit
        }

    def __init__(
            self, 
            element, 
            listitem,
            widgetmap,
            **kwargs):

        self.m_widgets={}
        self.m_map=widgetmap
        self.m_item=listitem
        self.m_element=element
        super().__init__(**kwargs)
        self.m_layout=QtWidgets.QGridLayout(self)
        self.setLayout(self.m_layout)
        self.setup()

    def setup(self):

        data=self.m_element.data()
        for n, d in self.m_map.items():
            k=d['w']
            p=[int(f) for f in d['p'].split('x')]
            w=self.wmap[k](parent=self)
            self.m_layout.addWidget(w, *p)
            self.m_widgets[n]=w
            t=str(data[n])
            self.set(n, t)

    def set(self, n, t):

        w=self.m_widgets[n]
        w.setText(str(t))
        w.adjustSize()
        self.adjustSize()

    def adjustSize(self):

        super().adjustSize()
        h=self.sizeHint()
        self.m_item.setSizeHint(h)
