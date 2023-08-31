from PyQt5 import QtCore, QtWidgets

from ..configure import Configure

class StatusBar(QtWidgets.QStatusBar):

    hideWanted=QtCore.pyqtSignal()
    toggled=QtCore.pyqtSignal(bool)
    keyPressed=QtCore.pyqtSignal(object)

    def __init__(self, window):

        super(StatusBar, self).__init__(
                objectName='Statusbar')

        self.window=window
        self.configure=Configure(
                app=window.app, 
                parent=self)

        self.setUI()

    def setUI(self):

        self.container=QtWidgets.QWidget(
                objectName='Statusbar_container')

        self.container_layout=QtWidgets.QVBoxLayout()

        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(0,0,0,0)

        self.container.setLayout(self.container_layout)

        self.bottom=QtWidgets.QWidget(
                objectName='Bottom')
        self.bottom.setFixedHeight(20)

        blayout=QtWidgets.QHBoxLayout()
        self.bottom.setLayout(blayout)

        blayout.setSpacing(0)
        blayout.setContentsMargins(0,0,0,0)

        self.mode=QtWidgets.QLabel(
                ':', objectName='Colon')
        self.edit=QtWidgets.QLineEdit(
                objectName='Edit')

        blayout.addWidget(self.mode)
        blayout.addWidget(self.edit)

        self.container_layout.addWidget(self.bottom)
        self.addPermanentWidget(self.container, 10)

        self.setContentsMargins(0,0,0,0)
        self.setSizeGripEnabled(False)
        self.bottom.hide()
