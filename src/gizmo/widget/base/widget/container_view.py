from PyQt5 import QtWidgets, QtCore

class ViewContainer(QtWidgets.QWidget):

    resized=QtCore.pyqtSignal()

    def __init__(self, 
                 view, 
                 objectName='ViewContainer',
                 **kwargs):

        super().__init__(
                objectName=objectName,
                **kwargs)

        self.m_layout=QtWidgets.QVBoxLayout()
        self.m_layout.setContentsMargins(
                0,0,0,0)
        self.setLayout(self.m_layout)
        self.insider=QtWidgets.QWidget(
                objectName='Holder'
                )
        self.insider.m_layout=QtWidgets.QHBoxLayout(
                self.insider)
        self.insider.m_layout.setContentsMargins(
                0,0,0,0)
        self.insider.setLayout(self.insider.m_layout)

        self.insider.m_layout.addWidget(view)
        self.m_layout.addWidget(self.insider)

        # self.resizeEvent=view.resizeEvent
        # self.insider.resizeEvent=view.resizeEvent

        view.container=self
        view.setFocus=self.setFocus
        view.setFocus=self.insider.setFocus

    @property
    def layoutMargin(self):

        return self.layout_margin

    @layoutMargin.setter
    def layoutMargin(self, margin):

        self.layout_margin=margin
        self.insider.m_layout.setContentsMargins(
                margin, margin, margin, margin)
