from PyQt5 import QtWidgets, QtCore

class TextEdit(QtWidgets.QTextEdit):

    widgetDataChanged=QtCore.pyqtSignal(object)

    def __init__(
            self,
            *args,
            index=None,
            wait_time=1000,
            **kwargs):

        self.m_index=index
        self.m_wait=wait_time
        self.m_reporting=False
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
        d={self.m_index: t}
        self.widgetDataChanged.emit(d)
