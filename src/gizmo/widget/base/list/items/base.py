from PyQt5 import QtWidgets, QtGui

class ItemWidget(QtWidgets.QWidget):

    def __init__(
            self, 
            listWidget, 
            data={},
            **kwargs,
            ):

        super().__init__(
                parent=listWidget,
                objectName='ListWidgetItem', 
                **kwargs
                )
        self.list=listWidget
        l=self.getLayout()
        self.setItem()
        self.setLayout(l)
        self.setData(data)

    def setItem(self):

        self.item = QtWidgets.QListWidgetItem(
                self.list)
        self.item.sizeHint=self.sizeHint
        self.item.widget=self

    def getLayout(self):

        self.up = QtWidgets.QLabel(
                objectName='Up')
        self.up.setWordWrap(True)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.up)
        layout.setContentsMargins(
                0, 0, 0, 0)
        self.up.hide()
        return layout 

    def setTextUp(self, text):

        self.up.show()
        self.up.setText(str(text))
        self.up.adjustSize()

    def textUp(self): 
        return self.up.text()

    def setData(self, data):

        self.data=data
        self.item.itemData=data
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
        self.item.setSizeHint(hint)

    def setFocus(self):
        self.up.setFocus()

    def select(self, cond):

        self.setProperty('selected', cond)
        self.up.style().unpolish(self.up)
        self.up.style().polish(self.up)
