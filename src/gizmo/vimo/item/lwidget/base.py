from PyQt5 import QtWidgets

class ListWidgetItem(QtWidgets.QWidget):

    def __init__(
            self, 
            listWidget, 
            data={},
            objectName='ListWidgetItem', 
            **kwargs,
            ):

        super().__init__(
                parent=listWidget,
                objectName=objectName,
                **kwargs)
        self.m_layout = QtWidgets.QVBoxLayout()
        self.m_list=listWidget
        self.m_data=data
        self.setup()

    def list(self):
        return self.m_list

    def setup(self):

        self.setListItem()
        self.setupLayout()
        self.setLayout(self.m_layout)
        self.setData(self.m_data)

    def listItem(self):
        return self.m_item

    def setListItem(self):

        self.m_item = QtWidgets.QListWidgetItem(
                self.m_list)
        self.m_item.sizeHint=self.sizeHint
        self.m_item.widget=self

    def setupLayout(self):

        layout = QtWidgets.QVBoxLayout()
        self.up = QtWidgets.QLabel(
                objectName='Up')
        self.up.setWordWrap(True)
        layout.setContentsMargins(
                0, 0, 0, 0)
        layout.addWidget(self.up)
        layout.setSpacing(0)
        self.m_layout=layout
        self.up.hide()

    def setTextUp(self, text):

        self.up.show()
        self.up.setText(str(text))
        self.up.adjustSize()

    def textUp(self): 
        return self.up.text()

    def setData(self, data):

        self.data=data
        self.m_item.itemData=data
        if data:
            if data.get('up', None): 
                text=str(data.get('up'))
                self.setTextUp(text)
            if data.get('up_style', None):
                style=data.get('up_style')
                self.up.setStyleSheet(style)
            self.adjustSize() 

    def adjustSize(self):

        super().adjustSize()
        hint=self.sizeHint()
        self.m_item.setSizeHint(hint)

    def setFocus(self):
        self.up.setFocus()

    def select(self, cond):

        raise
        self.setProperty('selected', cond)
        self.up.style().unpolish(self.up)
        self.up.style().polish(self.up)
