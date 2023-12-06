from PyQt5 import QtWidgets

class LineEdit(QtWidgets.QLineEdit):

    canEdit=True

    def __init__(
            self, 
            *args, 
            index=None,
            element=None,
            **kwargs):

        self.m_index=index
        self.m_element=element
        super().__init__(*args, **kwargs)
