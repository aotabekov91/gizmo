from PyQt5 import QtWidgets, QtCore, QtGui

class Overlay(QtWidgets.QWidget):

    def __init__(
            self,
            *args, 
            **kwargs
            ):

        self.blur=False
        super().__init__(
                *args, 
                **kwargs
                )

        self.setPalette(
                QtGui.QPalette(
                    QtCore.Qt.transparent)
                )
        self.setAttribute(
                QtCore.Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):

        if self.blur:
            qp = QtGui.QPainter()
            qp.begin(self)
            # Todo: move to style
            bcolor=QtGui.QColor(255, 255, 255, 200)
            qp.setBrush(bcolor)
            qp.drawRect(self.rect())
            qp.end()
        else:
            super().paintEvent(event)
