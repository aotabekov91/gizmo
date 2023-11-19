from PyQt5 import QtWidgets, QtCore

class Container(QtWidgets.QWidget):

    resized=QtCore.pyqtSignal()

    def __init__(self, 
                 obj, 
                 objectName='Container',
                 **kwargs):

        super().__init__(
                objectName=objectName, **kwargs)
        self.m_layout=QtWidgets.QVBoxLayout()
        self.m_layout.setContentsMargins(
                0,0,0,0)
        self.setLayout(self.m_layout)
        self.insider=QtWidgets.QWidget(
                objectName='Holder')
        self.insider.m_layout=QtWidgets.QHBoxLayout(
                self.insider)
        self.insider.m_layout.setContentsMargins(
                0,0,0,0)
        self.insider.setLayout(self.insider.m_layout)
        self.insider.m_layout.addWidget(obj)
        self.m_layout.addWidget(self.insider)
        self.resizeEvent=obj.resizeEvent
        self.insider.resizeEvent=obj.resizeEvent
        self.obj, obj.container=obj, self
