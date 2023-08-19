from PyQt5 import QtCore, QtWidgets

from ..configure import Configure

class StatusBar(QtWidgets.QStatusBar):

    hideWanted=QtCore.pyqtSignal()
    toggled=QtCore.pyqtSignal(bool)
    keyPressed=QtCore.pyqtSignal(object)

    def __init__(self, window):

        super(StatusBar, self).__init__(
                objectName='statusbar')

        self.window=window
        self.configure=Configure(
                app=window.app, 
                parent=self)

        self.setUI()

    def setUI(self):

        layout=self.layout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)

        self.container=QtWidgets.QWidget(
                objectName='statusbarContainer')

        self.container_layout=QtWidgets.QVBoxLayout()
        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container.setLayout(self.container_layout)

        self.bottom=QtWidgets.QWidget(
                objectName='statusbarBottom')
        self.bottom.setFixedHeight(20)

        blayout=QtWidgets.QHBoxLayout()
        self.bottom.setLayout(blayout)

        blayout.setSpacing(0)
        blayout.setContentsMargins(0,0,0,0)

        self.mode=QtWidgets.QLabel(
                ':', objectName='statusbarColon')
        self.edit=QtWidgets.QLineEdit(
                objectName='statusbarEdit')

        blayout.addWidget(self.mode)
        blayout.addWidget(self.edit)

        self.container_layout.addWidget(self.bottom)

        self.addPermanentWidget(self.container, 100)

        self.setSizeGripEnabled(False)

        self.bottom.hide()

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.mode.installEventFilter(listener)

    def removeEventFilter(self, listener):

        super().removeEventFilter(listener)
        self.mode.removeEventFilter(listener)

    def keyPressEvent(self, event):

        self.keyPressed.emit(event) 
        if event.key()==QtCore.Qt.Key_Escape: 
            self.hideWanted.emit() 
