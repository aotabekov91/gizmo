from PyQt5 import QtCore, QtGui, QtWidgets

class HintLabel(QtWidgets.QLabel):

    def __init__(
            self, 
            *args, 
            objectName='HintLabel',
            **kwargs):

        super().__init__(
                *args, 
                objectName=objectName,
                **kwargs)
        self.setAlignment(
                QtCore.Qt.AlignCenter)

    def resizeEvent(self, event):

        font = self.font()
        cRect = self.contentsRect()
        if self.text():
            fontSize = 1
            while True:
                f=font
                f.setPixelSize(fontSize)
                t=self.text()
                m = QtGui.QFontMetrics(f)
                r = m.boundingRect(t)
                c1= r.width() <= cRect.width()
                c2= r.height() <= cRect.height()
                if c1 and c2:
                    fontSize+=1
                else:
                    break
            font.setPixelSize(fontSize)
            self.setFont(font)
