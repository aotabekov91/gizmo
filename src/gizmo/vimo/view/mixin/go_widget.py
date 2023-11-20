from PyQt5 import QtCore

from .go_view import ViewGo

class WidgetGo(ViewGo):

    indexChanged=QtCore.pyqtSignal(object)

    def goto(self, digit=1):

        idx=self.getRowIndex(digit-1)
        self.setCurrentRow(digit-1)
        self.setCurrentIndex(idx)
