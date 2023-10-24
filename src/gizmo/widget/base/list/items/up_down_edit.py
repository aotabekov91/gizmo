from PyQt5 import QtCore, QtWidgets, QtGui
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

    def setItem(self):

        super().setItem()
        self.connect()

    def getLayout(self):

        layout =super().getLayout()
        self.down = QtWidgets.QTextEdit(
                objectName='Down')
        self.down.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.down.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        setEditorTabSize(self.down, 4)
        layout.addWidget(self.down, 70)
        return layout

    def connect(self):

        self.down.textChanged.connect(
                self.on_downChanged)

    def disconnect(self):

        self.down.textChanged.disconnect(
                self.on_downChanged)

    def setTextDown(self, text):

        self.down.show()
        self.down.setPlainText(text)
        self.down.adjustSize()
        self.setDownWidth()
        self.adjustDownSize()

    def setDownWidth(self):

        hint=self.up.size()
        doc=self.down.document()
        doc.setTextWidth(hint.width()-10)
        doc.adjustSize()

    def textDown(self): 
        return self.down.toPlainText()

    def adjustDownSize(self):

        doc=self.down.document()
        size=doc.size().toSize()
        height=max(40, size.height())
        self.down.setFixedHeight(
                height)
        self.item.setSizeHint(
                self.sizeHint())

    def setData(self, data):

        self.disconnect()
        super().setData(data)
        if data:
            text=data.get('down', '') 
            self.setTextDown(text)
            self.adjustSize()
        self.connect()

    def on_downChanged(self): 

        self.timer.stop()
        self.adjustDownSize()
        text=self.textDown()
        if text!=str(self.data['down']):
            self.data['down']=self.textDown()
            self.timer.start(500)

    def emitSignal(self):

        self.timer.stop()
        self.list.widgetDataChanged.emit(self)

    def setFocus(self): 

        self.down.setFocus()
        self.setCursorAtEnd()

    def setCursorAtEnd(self):

        cur=self.down.textCursor()
        cur.movePosition(
                QtGui.QTextCursor.End)
        self.down.setTextCursor(cur)

    def select(self, cond):

        super().select(cond)
        self.down.style().unpolish(self.down)
        self.down.style().polish(self.down)
