from PyQt5 import QtWidgets, QtCore

from .line import LineEdit

class InputLineEdit(QtWidgets.QWidget):

    textChanged=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()

    def __init__(
            self, 
            *args, 
            objectName='InputLine',
            **kwargs): 

        super().__init__(
                *args, 
                objectName=objectName,
                **kwargs) 
        self.setupUI()

    def setupUI(self):

        self.m_label= QtWidgets.QLabel(
                objectName='InputLabel')
        layout=QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.m_label)

        self.m_input_label=QtWidgets.QWidget(
                objectName='InputLabelContainer')
        self.m_input_label.setLayout(layout)
        self.m_edit=LineEdit(self)
        layout=QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.m_edit)

        self.m_input_edit=QtWidgets.QWidget(
                self, objectName='LineEditContainer')
        self.m_input_edit.setLayout(layout)

        layout  = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(3,3,3,3)
        layout.addWidget(self.m_input_label, 10)
        layout.addWidget(self.m_input_edit, 90)

        self.m_container=QtWidgets.QWidget(
                objectName='InputLineContainer')
        self.m_container.setLayout(layout)
        layout=QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.m_container)

        self.setLayout(layout)

        self.m_edit.textChanged.connect(
                self.textChanged)
        self.m_edit.returnPressed.connect(
                self.returnPressed)
        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)
        self.setFixedHeight(50)
        self.adjustSize()

    def adjustSize(self):

        self.m_edit.adjustSize()
        super().adjustSize()

    def hideLabel(self):

        self.m_label.hide()
        self.m_input_label.hide()

    def showLabel(self):

        self.m_label.show()
        self.m_input_label.show()

    def label(self): 
        return self.m_label.text()

    def setLabel(self, label):

        self.m_label.setText(label)
        self.m_label.setAlignment(Qt.AlignCenter)
        self.showLabel()

    def text(self): 
        return self.m_edit.text()

    def setText(self, text): 
        self.m_edit.setText(text)

    def clear(self): 
        self.m_edit.clear()

    def setFocus(self): 
        self.m_edit.setFocus()
