from PyQt5 import QtWidgets, QtCore

class TextEdit(QtWidgets.QTextEdit):

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
        self.setTimer()

    def setTimer(self):

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                self.reportChange)
        self.m_reporting=True

    def on_textChanged(self):

        self.timer.stop()
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
