from PyQt5 import QtWidgets, QtCore
from gizmo.utils import setEditorTabSize

class TextEdit(QtWidgets.QTextEdit):

    canEdit=True

    def __init__(
            self,
            *args,
            index=None,
            parent=None,
            element=None,
            wait_time=1000,
            **kwargs):

        self.m_index=index
        self.m_parent=parent
        self.m_wait=wait_time
        self.m_reporting=False
        self.m_element=element
        super().__init__(
                *args, **kwargs)
        self.textChanged.connect(
                self.on_textChanged)
        setEditorTabSize(self, 4)
        self.setStyleSheet(
                'background-color: blue;')
        self.setTimer()
        self.setBars()

    def setTimer(self):

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                self.reportChange)
        self.m_reporting=True

    def on_textChanged(self):

        self.timer.stop()
        self.adjustSize()
        if self.m_reporting:
            self.timer.start(self.m_wait)

    def reportChange(self):

        self.timer.stop()
        t=self.toPlainText()
        d=self.m_element.data()
        d.update({self.m_index: t})
        p=self.m_parent
        if p:
           p.widgetDataChanged.emit(
                   self.m_element)

    def sizeHint(self):

        h=super().sizeHint()
        doc=self.document()
        size=doc.size().toSize()
        height=max(25, size.height())
        h.setHeight(height)
        h.setWidth(h.width()-25)
        return h

    # def readjust(self):
    #     return
    #     print(self.size())
    #     # self.adjustSize()
    #     h=self.sizeHint()
    #     self.setFixedSize(h)
    #     self.m_parent.adjustSize()
    #     self.m_parent.adjustSizeHint()
        
        # print(h)
        # print(size)
        # self.setFixedHeight(height)
        # s=self.size()
        # print(s, size)
        # self.resize(s)
        # self.resize(size)
        # self.adjustSize()
        # self.m_parent.adjustSize()
        # self.m_parent.adjustSizeHint()

    def setBars(self):

        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
