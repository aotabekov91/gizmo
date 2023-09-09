from PyQt5 import QtCore, QtWidgets

from ..configure import Configure

class StatusBar(QtWidgets.QStatusBar):

    hideWanted=QtCore.pyqtSignal()
    toggled=QtCore.pyqtSignal(bool)
    keyPressed=QtCore.pyqtSignal(object)

    def __init__(self, 
                 window,
                 objectName='Statusbar',
                 ):

        super(StatusBar, self).__init__(
                objectName=objectName)

        self.window=window
        self.configure=Configure(
                app=window.app, 
                parent=self)
        self.setUI()

    def setUI(self):

        self.container=QtWidgets.QWidget(
                objectName='Container')
        self.container.setContentsMargins(0,0,0,0)

        self.container_layout=QtWidgets.QVBoxLayout(
                self.container)

        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container.setLayout(self.container_layout)

        self.bottom=QtWidgets.QWidget(objectName='Bottom')

        blayout=QtWidgets.QHBoxLayout(self.bottom)
        blayout.setSpacing(0)
        blayout.setContentsMargins(0,0,0,0)

        self.mode=QtWidgets.QLabel(
                ':', objectName='Mode')
        self.edit=QtWidgets.QLineEdit(
                objectName='Edit')

        blayout.addWidget(self.mode)
        blayout.addWidget(self.edit)
        self.bottom.setLayout(blayout)

        self.container_layout.addWidget(self.bottom)
        self.addPermanentWidget(self.container, 10)

        self.setContentsMargins(0,0,0,0)
        self.setSizeGripEnabled(False)
        self.bottom.hide()
