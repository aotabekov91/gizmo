from PyQt5 import QtWidgets

class LineEdit(QtWidgets.QLineEdit):

    def __init__(
            self, 
            *args, 
            index=None,
            **kwargs):

        self.m_index=index
        super().__init__(*args, **kwargs)
