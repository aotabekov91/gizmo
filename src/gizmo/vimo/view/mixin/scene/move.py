from PyQt5 import QtCore
from .base import Scene

class MoveScene(Scene):

    canMove=True
    positionChanged=QtCore.pyqtSignal()

    def screenLeft(self, digit=1):
        self.moveScreen('left', digit)
        
    def screenRight(self, digit=1):
        self.moveScreen('right', digit)

    def screenUp(self, digit=1):
        self.moveScreen('up', digit)

    def screenDown(self, digit=1):
        self.moveScreen('down', digit)

    def down(self, digit=1):
        self.move('down', digit)

    def up(self, digit=1):
        self.move('up', digit)

    def left(self, digit=1):
        self.move('left', digit)

    def right(self, digit=1):
        self.move('right', digit)

    def moveScreen(self, kind, digit=1):

        s=self.size()
        h, w=s.height(), s.width()
        sr=self.scene().sceneRect()
        sh, sw = sr.height(), sr.width()
        vb=self.verticalScrollBar()
        hb=self.horizontalScrollBar()
        if self.check('hasLayout'):
            h=self.m_layout.height(h)
            w=self.m_layout.height(w)
        if kind=='screenUp':
            dx=vb.value() - h*digit
            dx=max(0, dx) 
            vb.setValue(int(dx))
        elif kind=='screenDown':
            dx=vb.value() + h*digit
            dx=min(sh, dx) 
            vb.setValue(int(dx))
        elif kind=='screenLeft':
            dy=hb.value() - w*digit
            dy=max(0, dy) 
            hb.setValue(int(dy))
        elif kind=='screenRight':
            dy=hb.value() + w*digit
            dy=min(sw, dy) 
            hb.setValue(int(dy))
        self.setVisibleItem()
        self.positionChanged.emit()

    def move(self, kind, digit=1):

        if 'screen' in kind:
            return self.moveScreen(kind, digit)
        s=self.size()
        h, w=s.height(), s.width()
        sr=self.scene().sceneRect()
        vb=self.verticalScrollBar()
        hb=self.horizontalScrollBar()
        if self.check('hasLayout'):
            h=self.m_layout.height(h)
            w=self.m_layout.height(w)
        h=h*self.zoomFactor
        w=w*self.zoomFactor
        if kind=='down':
            dx=vb.value() + h*digit
            dx=min(sr.height(), dx)
            vb.setValue(int(dx))
        elif kind=='up':
            dx=vb.value() - h*digit
            dx=max(0, dx)
            vb.setValue(int(dx))
        elif kind=='right':
            dx=hb.value() + w*digit
            hb.setValue(int(dx))
        elif kind=='left':
            dx=hb.value() - w*digit
            hb.setValue(int(dx))
        self.setVisibleItem()
        self.positionChanged.emit()
