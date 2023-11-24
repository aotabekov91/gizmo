from PyQt5 import QtWidgets, QtCore

from .move import Move

class ViewMove(Move):

    def _move(self, arg):

        m=getattr(QtWidgets.QAbstractItemView, arg, None)
        if m:
            i=self.moveCursor(m, QtCore.Qt.NoModifier)
            self.setCurrentIndex(i)

    def move(self, kind, digit=1):


        func=None
        if kind=='up':
            func=lambda: self._move('MoveUp')
        elif kind=='down':
            func=lambda: self._move('MoveDown')
        else:
            func=self._move(kind)
        if func:
            for i in range(digit): 
                func()
