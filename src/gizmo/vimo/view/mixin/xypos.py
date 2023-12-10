from PyQt5 import QtCore

class XYPos:

    canJump=True
    canPosition=True
    positionJumped=QtCore.pyqtSignal()
    positionChanged=QtCore.pyqtSignal()

    def getPosition(self, data=None, kind=None):

        if self.m_curr and self.m_items:
            i=self.m_items[self.m_curr]
            r=i.boundingRect().translated(i.pos())
            tl=self.viewport().rect().topLeft()
            tl=self.mapToScene(tl)
            x=(tl.x() -r.x())/r.width()
            y=(tl.y() -r.y())/r.height()
            return self.m_curr, x, y
        return 1, 0, 0

    def goTo(self, digit=1, x=0, y=0):

        if digit is None:
            self.goToLast()
        else:
            self.jumpToPos(digit, x, y)
            self.positionJumped.emit()
            self.positionChanged.emit()

    def redraw(self, pos=None):

        pos = pos or self.getPosition()
        self.redrawScene()
        self.jumpToPos(*pos)

    def jumpToPos(self, *pos):

        self.updatePosition(*pos)
        self.setVisibleItem()
        self.viewport().update()

    def updatePosition(self, digit=1, x=0, y=0):

        v, h = 0, 0
        i=self.m_items.get(digit, None)
        if i:
            r = i.boundingRect()
            p = r.translated(i.pos())
            h = int(p.left()+x*p.width())
            v = int(p.top()+y*p.height())
            self.horizontalScrollBar().setValue(h)
            self.verticalScrollBar().setValue(v)
