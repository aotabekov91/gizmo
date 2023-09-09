from PyQt6 import QtCore, QtWidgets

from ..base import TreeWidget, InputLabelWidget

class InputTree (QtWidgets.QWidget):

    hideWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    inputTextChanged=QtCore.pyqtSignal()
    inputReturnPressed=QtCore.pyqtSignal()

    keysChanged=QtCore.pyqtSignal(str)
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(self, 
            *args, 
            set_base_style=True,
            **kwargs): 

        super(InputTree, self).__init__()

        self.set_base_style=set_base_style

        layout, style_sheet=self.setUI()
        self.setLayout(layout)

        # if self.set_base_style:
        #     self.setStyleSheet(style_sheet)

        self.setMinimumSize(400, 600)
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
        self.tree=TreeWidget(
                set_base_style=self.set_base_style,
                )
        self.input=InputLabelWidget()
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
