from gizmo.utils import tag
from PyQt5 import QtWidgets, QtCore

from .move import Move

class ViewMove(Move):

    @tag('e', modes=['normal|TreeView'])
    def expandAll(self):
        super().expandAll()

    @tag('c', modes=['normal|TreeView'])
    def collapseAll(self):
        super().collapseAll()

    @tag('H', modes=['normal|TreeView'])
    def collapseAllInside(self):
        super().collapseAllInside()

    @tag('d', modes=['normal|TreeView'])
    def rootDown(self, digit=1):
        super().rootDown(digit)

    @tag('u', modes=['normal|TreeView'])
    def rootUp(self, digit=1):
        super().rootUp(digit)

    def move(self, kind, digit=1):

        def _move(arg):
            m=getattr(QtWidgets.QAbstractItemView, arg)
            i=self.moveCursor(m, QtCore.Qt.NoModifier)
            self.setCurrentIndex(i)

        func=None
        if kind=='up':
            func=lambda: _move('MoveUp')
        elif kind=='down':
            func=lambda: _move('MoveDown')
        if func:
            for i in range(digit): 
                func()
