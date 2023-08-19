from PyQt5 import QtCore, QtWidgets

from ..configure import Configure

class StatusBar(QtWidgets.QStatusBar):

    hideWanted=QtCore.pyqtSignal()
    toggled=QtCore.pyqtSignal(bool)
    keyPressed=QtCore.pyqtSignal(object)

    def __init__(self, window):

        super(StatusBar, self).__init__()

        self.window=window
        self.configure=Configure(
                app=window.app, 
                parent=self)

        self.setUI()

    def setUI(self):

        self.style_sheet='''
            QLineEdit {
                background-color: transparent;
                border-color: transparent;
                border-width: 0px;
                border-radius: 0px;
                }
            QLabel{
                background-color: transparent;
                }
                '''

        layout=self.layout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.mode=QtWidgets.QLabel(':')
        self.edit=QtWidgets.QLineEdit(self)

        self.setFixedHeight(25)

        self.addPermanentWidget(self.mode)
        self.addPermanentWidget(self.edit, 100)

        self.setSizeGripEnabled(False)
        self.setStyleSheet(self.style_sheet)

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
