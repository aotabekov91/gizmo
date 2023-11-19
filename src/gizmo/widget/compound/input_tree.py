from PyQt5 import QtCore, QtWidgets

from ..base import TreeView, InputLineEdit

class InputTree(QtWidgets.QWidget):

    hideWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    keysChanged=QtCore.pyqtSignal(str)
    inputTextChanged=QtCore.pyqtSignal()
    inputReturnPressed=QtCore.pyqtSignal()
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(
            self, 
            *args, 
            **kwargs
            ): 

        super().__init__(
                *args, 
                **kwargs
                )
        layout, style_sheet=self.setUI()
        self.setLayout(layout)
        self.input.hide()
        self.setup()

    def setup(self):

        self.tree.keyPressed.connect(
                self.keyPressed)
        self.tree.keysChanged.connect(
                self.keysChanged)

    def setUI(self):

        style_sheet='''
            QWidget{
                font-size: 15px;
                color: white;
                border-width: 0px;
                background-color: #101010; 
                border-color: transparent;
                }
            QWidget#mainWidget{
                border-radius: 10px;
                border-style: outset;
                background-color: transparent; 
                }
                '''
        self.tree=TreeView()
        self.input=InputLineEdit()
        self.tree.hideWanted.connect(
                self.hideWanted)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.input)
        layout.addWidget(self.tree)
        return layout, style_sheet

    def installEventFilter(self, treeener):

        self.tree.installEventFilter(treeener)
        self.input.installEventFilter(treeener)

    def setFocus(self): self.tree.setFocus()

    def toggleInput(self):

        if self.input.isVisible():
            self.input.hide()
            self.tree.setFocus()
        else:
            self.input.show()
            self.input.setFocus()

    def keyPressEvent(self, event):

        if event.modifiers():
            if event.key() in [QtCore.Qt.Key_BracketLeft]:
                self.hideWanted.emit()
            elif event.key() in [QtCore.Qt.Key_I]:
                self.toggleInput()
        else:
            super().keyPressEvent(event)
