from PyQt5 import QtWidgets

class BaseListWidget(QtWidgets.QLabel):

    def __init__(
            self, element, **kwargs,):

        super().__init__(**kwargs)
        self.m_element=element
        self.setup()

    def setup(self):

        data=self.m_element.data()
        idx=str(data['id'])
        self.setText(idx)
