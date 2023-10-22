from PyQt5 import QtCore, QtWidgets
from gizmo.utils import setEditorTabSize

from .base import ItemWidget

class UpDownEdit (ItemWidget):

    def __init__(
            self, 
            *args, 
            **kwargs
            ):

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                self.emitSignal)
        super().__init__(
                *args, **kwargs)

    def getLayout(self):

        layout =super().getLayout()
        self.down = QtWidgets.QTextEdit(
                objectName='downEdit')
        self.down.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.down.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.down.textChanged.connect(
                self.on_downChanged)
        setEditorTabSize(self.down, 4)
        layout.addWidget(self.down, 70)
        return layout

    def setTextDown(self, text):

        self.down.show()
        self.down.setPlainText(text)
        self.down.adjustSize()

    def textDown(self): 
        return self.down.toPlainText()

    def setDownSize(self):

        doc=self.down.document()
        doc.adjustSize()
        size=doc.size().toSize()
        self.down.setFixedHeight(
                size.height())

    def setData(self, data):

        super().setData(data)
        if data:
            if data.get('down', None): 
                text=str(data.get('down'))
                self.setTextDown(text)
            self.adjustSize()

    def on_downChanged(self): 

        self.timer.stop()
        text=self.textDown()
        self.setDownSize()
        if text!=str(self.data['down']):
            self.data['down']=self.textDown()
            self.timer.start(500)

    def emitSignal(self):

        self.timer.stop()
        self.list.widgetDataChanged.emit(self)

    def setFocus(self): 
        self.down.setFocus()
