from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontMetrics

class HintLabel(QLabel):

    def __init__(self, 
                 *args, 
                 objectName='HintLabel',
                 **kwargs):

        super().__init__(
                *args, 
                objectName=objectName,
                **kwargs)
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):

        font = self.font()
        cRect = self.contentsRect()
        if self.text():
            fontSize = 1
            while True:
                f=font
                f.setPixelSize(fontSize)
                r = QFontMetrics(f).boundingRect(self.text())
                if r.height() <= cRect.height() and r.width() <= cRect.width():
                    fontSize+=1
                else:
                    break
            font.setPixelSize(fontSize)
            self.setFont(font)
