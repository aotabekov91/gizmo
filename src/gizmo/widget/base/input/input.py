from PyQt5 import QtCore, QtWidgets

class InputWidget(QtWidgets.QLineEdit):

    hideWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()

    def __init__ (
            self, 
            *args, 
            objectName='InputLineEdit',
            **kwargs
            ): 

        super().__init__(
                *args, 
                objectName=objectName,
                **kwargs
                ) 

        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)

    def setLabel(self, text):
        self.setPlaceholderText(text)

    def hideLabel(self):
        self.clear()
