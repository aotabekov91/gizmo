from PyQt5 import QtWidgets

class Item(QtWidgets.QWidget):

    def __init__(
            self, 
            listWidget, 
            data={},
            **kwargs,
            ):

        super(Item, self).__init__(
                parent=listWidget,
                objectName='ListItemWidget', 
                **kwargs
                )

        self.list=listWidget
        layout, style_sheet=self.setUI()
        self.setLayout(layout)
        self.setItem()
        self.setData(data)

    def setItem(self):

        self.item = QtWidgets.QListWidgetItem(
                self.list)
        self.item.sizeHint=self.sizeHint
        self.item.widget=self

    def setUI(self):

        style_sheet = '''
            QWidget{
                color: white;
                border-width: 0px;
                }
            QLabel{
                border-radius: 10px;
                border-style: outset;
                padding: 2px 10px 2px 10px;
                }
                '''

        self.up = QtWidgets.QLabel(
                objectName='ListItemUp')
        self.up.setWordWrap(True)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.up)
        layout.setContentsMargins(4, 4, 4, 4)
        return layout, style_sheet

    def setTextUp(self, text):

        self.up.show()
        self.up.setText(str(text))
        self.up.adjustSize()

    def textUp(self): 
        return self.up.text()

    def listItem(self): 
        return self.item

    def setData(self, data):

        self.data=data
        self.item.itemData=data
        if data:
            if data.get('up', None): 
                self.setTextUp(str(data.get('up')))
            style=data.get('style', None)
            if style:
                style=str(style).replace("'", "")
                self.style_sheet+style
                self.setStyleSheet(style)
            up_color=data.get('style', None)
            if up_color: 
                up_style=self.label_style+f'color: black; background-color: {up_color};'+'}'
                self.up.setStyleSheet(up_style)
            color=data.get('item_color', None)
            if color: 
                self.style_sheet+='QWidget {background-color: '+f'{color}; '+' color: black}'
                self.setStyleSheet(self.style_sheet)

    def setFixedWidth(self, width):

        if hasattr(self, 'up'): 
            self.up.setFixedWidth(width-12) # minus padding
        super().setFixedWidth(width)
        self.adjustSize()

    def adjustSize(self):

        super().adjustSize()
        self.item.setSizeHint(self.sizeHint())

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.up.installEventFilter(listener)

    def on_contentChanged(self): 
        self.list.widgetDataChanged.emit(self)
