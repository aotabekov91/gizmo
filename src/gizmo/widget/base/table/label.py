from PyQt5 import QtWidgets

class Label(QtWidgets.QLabel):

    def __init__(
            self,
            *args,
            index=None, 
            element=None,
            **kwargs):

        self.m_index=index
        self.m_element=element
        super().__init__(
                *args, **kwargs)
