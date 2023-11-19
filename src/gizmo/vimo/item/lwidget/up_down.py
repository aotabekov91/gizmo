from PyQt5 import QtWidgets

from .base import ListWidgetItem

class UpDown(ListWidgetItem):

    def getLayout(self):

        layout = super().getLayout()
        self.down = QtWidgets.QLabel(
                objectName='downElement')
        self.down.setWordWrap(True)
        layout.removeWidget(self.up)
        layout.addWidget(self.up, 50)
        layout.addWidget(self.down, 50)
        layout.addStretch()
        self.up.hide()
        self.down.hide()
        return layout

    def setTextDown(self, text):

        self.down.setText(str(text))
        self.down.show()
        self.down.adjustSize()

    def textDown(self): 
        return self.down.text()

    def setData(self, data):

        super().setData(data)
        if data:
            if data.get('down', None):
                self.setTextDown(str(data.get('down')))
                color=data.get('down_color', None)

                # if color: 
                #     self.setStyleSheet(
                #             self.style_sheet + ' '.join(
                #         ['QLabel#downElement{',
                #          f'background-color: {color};',
                #          'color: black;}',
                #          ]))

        self.adjustSize()

    def sizeHint(self):

        size=super().sizeHint()
        upsize=self.up.size()
        size.setWidth(upsize.width())
        return size
