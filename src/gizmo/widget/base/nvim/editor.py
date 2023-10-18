from gizmo.utils import setEditorTabSize
from PyQt5 import QtWidgets, QtGui, QtCore

from gizmo.widget.base.nvim import NVim

class VimEditor(QtWidgets.QTextEdit):

    def __init__(
            self, 
            bar=None, 
            nvim=NVim, 
            parent = None, 
            tab_stop = 4,
            font='MS Gothic'
            ):

        super().__init__(
                parent=parent, 
                objectName='NVimEditor'
                )

        self.bar = bar
        self.nvim = nvim
        self.abort = False
        self.tab_stop=tab_stop
        self.setFont(QtGui.QFont(font))
        setEditorTabSize(self, self.tab_stop)

    def keyPressEvent(self, e):

        key = e.text()
        if key:
            self.nvim.keyPress(key)
            while self.nvim.isBlocked():
                QtWidgets.QApplication.processEvents()
                if self.abort: return
            self.update()

    def text(self):

        return self.nvim.text()

    def clear(self):

        super().clear()
        self.nvim.setText('')

        #TODO: instead of jk [which is custom-specific] send Escape to return to normal mode from insert mode
        self.nvim.keyPress('jk') 

    def update(self):

        self.setPlainText(self.nvim.text())
        mode = self.nvim.mode()
        row, col = self.nvim.cursorPosition()
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(self.nvim.byte(row, col))
        self.setTextCursor(cursor)
        selections = []
        cond=mode != 'i' 
        cond=cond and mode != 'v' 
        cond=cond and mode != 'V' 
        cond=cond and mode != '' 
        cond=cond and mode[0] != 'c'

        if mode=='i':
            self.setCursorWidth(1)
        elif mode=='n':
            self.setCursorWidth(0)
        
        if cond:
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.cursor.movePosition(
                    QtGui.QTextCursor.NextCharacter, 
                    QtGui.QTextCursor.KeepAnchor)
            selection.format = QtGui.QTextCharFormat()
            selection.format.setBackground(QtCore.Qt.black)
            selection.format.setForeground(QtCore.Qt.white)
            selections.append(selection)

        if mode == 'v' or mode == 'V' or mode == '':

            row2, col2 = self.nvim.cursorAnchor()
            if row2 > 0 and col2 >= 0:
                begin = self.nvim.byte(row, col)
                end = self.nvim.byte(row2, col2)

                if end <= begin + 1:
                    begin += 1
                    end -= 1

                selection = QtWidgets.QTextEdit.ExtraSelection()

                selection.cursor = QtGui.QTextCursor(self.document())

                selection.cursor.setPosition(begin)
                if mode == 'V':
                    if begin <= end:
                        selection.cursor.movePosition(
                                QtGui.QTextCursor.StartOfBlock)
                    else:
                        selection.cursor.movePosition(
                                QtGui.QTextCursor.EndOfBlock)

                selection.cursor.setPosition(
                        end, QtGui.QTextCursor.KeepAnchor)
                if mode == 'V':
                    if end <= begin:
                        selection.cursor.movePosition(
                                QtGui.QTextCursor.StartOfBlock,
                                QtGui.QTextCursor.KeepAnchor)
                    else:
                        selection.cursor.movePosition(
                                QtGui.QTextCursor.EndOfBlock,
                                QtGui.QTextCursor.KeepAnchor)

                selection.format = QtGui.QTextCharFormat()
                selection.format.setBackground(QtCore.Qt.black)
                selection.format.setForeground(QtCore.Qt.white)
                selections.append(selection)

        self.setExtraSelections(selections)

        bar_data={'info': f"[{mode}]"}
        cmd=self.nvim.commandLine()
        if cmd: bar_data['detail']=cmd
        self.bar.setData(bar_data)