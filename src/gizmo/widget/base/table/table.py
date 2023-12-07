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
    hasWidgets=True
    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            wmap={},
            item=None,
            view=None,
            element=None, 
            objectName='GridWidget',
            **kwargs
            ):

        self.m_view=view
        self.m_wmap=wmap
        self.m_item=item
        self.m_widgets={}
        self.m_element=element
        super().__init__(
                objectName=objectName, **kwargs)
        self.setup()
        self.setData()

    def setListItem(self, item):
        self.m_item=item

    def setup(self):
        
        self.m_element.dataUpdated.connect(
                self.updateData)
        l=QtWidgets.QGridLayout(self)
        l.setContentsMargins(10, 10, 10, 10)
        l.setSpacing(0)
        self.setLayout(l)
        self.m_layout=l

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

    def widgets(self):
        return self.m_widgets

    def updateData(self):

        d=self.m_element.data()
        for n in self.m_widgets.keys():
            self.set(n, str(d[n]))

    # def setView(self, v):

    #     self.reconnect('disconnect')
    #     self.m_view=v
    #     self.reconnect()

    # def reconnect(self, kind='connect'):

    #     v=self.m_view
    #     if not v: return
    #     s=getattr(v, 'resized', None)
    #     if not s: return
    #     f=getattr(s, kind, None)
    #     if f: f(self.adjustSizeHint)

    def set(self, n, t):

        w = self.m_widgets[n]
        w.m_reporting=False
        w.setText(str(t))
        w.m_reporting=True

    def adjustSizeHint(self):

        if self.m_item:
            self.adjustSize()
            p=self.parent()
            for i in self.m_widgets.values():
                i.adjustSize()
            h=self.sizeHint()
            h.setWidth(h.width())
            self.m_item.setSizeHint(h)
