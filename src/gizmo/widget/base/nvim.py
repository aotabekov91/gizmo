import pynvim
import tempfile

from PyQt6 import QtWidgets, QtGui, QtCore

from gizmo.utils import setEditorTabSize

class NVim ():

    def __init__(self):
        self.nvim = pynvim.attach(
                'child', 
                argv=[
                    '/bin/env', 
                    'nvim', 
                    '--embed', 
                    '--headless'
                    ])

        self.inputDoneFile = tempfile.NamedTemporaryFile()
        self.inputId = 0

    def setText(self, text):
        self.buffer()[:] = text.split('\n')

    def text(self):
        return '\n'.join(self.buffer()[:])

    def buffer(self):
        return self.nvim.current.buffer

    def cursorPosition(self):
        return self.nvim.windows[0].cursor

    def cursorAnchor(self):
        return [self.nvim.eval('line("v")'), 
                self.nvim.eval('col("v")')]

    def keyPress(self, key):
        self.nvim.input(key)

        self.inputId += 1
        self.nvim.call('writefile', 
                       [self.inputId], 
                       self.inputDoneFile.name, 
                       async_=True)

    def mode(self):
        return self.eval('mode()')

    def commandLine(self):
        return self.eval('getcmdline()')

    def commandLineType(self):
        return self.eval('getcmdtype()')

    def byte(self, row, col):

        cmd='line2byte(' + str(row) + ')'
        return self.eval(cmd) + col - 1

    def eval(self, expr):
        return self.nvim.eval(expr)

    def isBlocked(self):
        with open(self.inputDoneFile.name, 'r') as f:
            data = f.read().strip()
            return data != str(self.inputId)
        return False

class Editor (QtWidgets.QTextEdit):

    """ Editor widget driven by FakeVim. """

    def __init__(self, 
                 nvim, 
                 bar, 
                 parent = None,
                 tab_stop = 4
                 ):

        sup = super(Editor, 
                    self,
                    objectName='NVimEditor'
                    )
        sup.__init__(parent)

        # self.setStyleSheet('''
        #     QWidget{
        #         font-size: 16px;
        #         color: white;
        #         border-radius: 15px;
        #         border-style: outset;
        #         background-color: rgba(0, 0, 0, .8); 
        #         padding: 15px 15px 15px 15px;
        #         }
        #     ''')

        self.setFont(QtGui.QFont("MS Gothic"))
        self.bar = bar
        self.nvim = nvim
        self.abort = False
        self.tab_stop=tab_stop

        self.setup()

    def setup(self): 

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
