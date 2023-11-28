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

    def comparePosition(
            self, digit=None, x=0, y=0):

        c = self.count() 
        cx, cy, ci = self.getPosition()
        p = digit or c 
        if 0 < p <= c:
            cp=self.m_layout.current(p)
            cc = self.m_curr != cp 
            cc = any([cc, abs(x-cx) > 0.001])
            cc = any([cc, abs(y-cy) > 0.001])
            return cc

    def goto(self, digit=1, x=0, y=0):

        self.redrawView(digit, x, y)
        self.setVisibleItem()
        self.positionJumped.emit()
        self.positionChanged.emit()

    def redraw(self):

        pos = self.getPosition()
        self.redrawScene()
        self.redrawView(*pos)
        self.setVisibleItem()

    def redrawView(self, digit=1, x=0, y=0):

        vv, hv = 0, 0
        s = self.scene()
        r = s.sceneRect()
        l, t = r.left(), r.top()
        w, h = r.width(), r.height()
        for j, i in self.m_items.items():
            pbr = i.boundingRect()
            pos = pbr.translated(i.pos())
            if self.continuousMode:
                i.setVisible(True)
            else:
                if self.m_layout.left(j) == self.m_curr:
                    i.setVisible(True)
                    t = pos.top()
                    h = pos.height()
                else:
                    i.setVisible(False)
                    i.cancelRender()
            if j == digit:
                hv = int(pos.left()+x*pos.width())
                vv = int(pos.top()+y*pos.height())
        self.setSceneRect(l, t, w, h)
        self.horizontalScrollBar().setValue(hv)
        self.verticalScrollBar().setValue(vv)
        self.viewport().update()
