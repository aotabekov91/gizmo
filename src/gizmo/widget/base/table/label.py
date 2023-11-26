from PyQt5 import QtWidgets

class Label(QtWidgets.QLabel):

    def __init__(
            self,
            *args,
            index=None, 
            **kwargs):

        self.m_index=index
        super().__init__(
                *args, **kwargs)
