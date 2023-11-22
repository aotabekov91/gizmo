import re
from PyQt5 import QtWidgets, QtCore

from ..base import ListWidget, LineEdit

class InputList(QtWidgets.QWidget):

    openWanted=QtCore.pyqtSignal()
    hideWanted=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    inputTextChanged=QtCore.pyqtSignal()
    inputReturnPressed=QtCore.pyqtSignal()
    listReturnPressed=QtCore.pyqtSignal()

    def __init__(
            self, 
            list_class=ListWidget, 
            objectName='InputList',
            input_class=LineEdit, 
            regex_func=None,
            **kwargs
            ): 

        self.regex_func=regex_func
        super().__init__(
                objectName=objectName)

        self.setInputWidget(
                input_class)
        self.setListWidget(
                list_class, **kwargs)
        self.kwargs=kwargs
        self.setupUI()

    def setListWidget(
            self, 
            list_class, 
            **kwargs
            ):

        if list_class:
            self.list=list_class(
                    **kwargs)
            self.list.hideWanted.connect(
                    self.hideWanted)
            self.list.openWanted.connect(
                    self.openWanted)
            self.list.returnPressed.connect(
                    self.returnPressed)
            self.list.returnPressed.connect(
                    self.listReturnPressed)

    def setInputWidget(
            self, 
            input_class
            ):

        if input_class:
            self.input=input_class()
            self.input.hideWanted.connect(
                    self.hideWanted)
            self.input.returnPressed.connect(
                    self.returnPressed)
            self.input.returnPressed.connect(
                    self.inputReturnPressed)
            self.input.textChanged.connect(
                    self.updateInputText)
            self.input.textChanged.connect(
                    self.inputTextChanged)
            self.input.setLabel('Filter')
            self.input.hide()

    def setupUI(self):

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(
                0, 0, 0, 0)
        layout.addWidget(self.input)
        layout.addWidget(self.list)
        self.setLayout(layout)

    def setList(self, dlist): 
        self.list.setList(dlist)

    def updateInputText(self, text):

        if self.regex_func:
            fields, flags=self.regex_func()
        else:
            flags=re.I
            fields={'up': f'.*{text}.*'}
        self.filter(
                flags=flags,
                fields=fields
                )

    def filter(
            self, 
            flags=0,
            fields={}, 
            ):

        self.list.filter(
                flags=flags, 
                fields=fields)

    def setFocus(self):

        if self.input.isVisible():
            self.input.setFocus()
        else:
            self.list.setFocus()

    def toggleFilter(self):

        if self.input.hasFocus():
            self.input.hide()
        else:
            self.input.show()
        self.setFocus()
