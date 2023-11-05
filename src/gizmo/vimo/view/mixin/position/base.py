class PosMixin:

    canPosition=True

    def getPos(self):

        if self.m_curr:
            i=self.m_items[self.m_curr]
            r=i.boundingRect().translated(i.pos())
            tl=self.viewport().rect().topLeft()
            tl=self.mapToScene(tl)
            x=(tl.x() -r.x())/r.width()
            y=(tl.y() -r.y())/r.height()
            return self.m_curr, x, y
        return 1, 0, 0

    def comPos(
            self, digit=None, x=0, y=0):

        c = self.count() 
        cx, cy, ci = self.getPos()
        p = digit or c 
        if 0 < p <= c:
            cp=self.m_layout.current(p)
            cc = self.m_curr != cp 
            cc = any([cc, abs(x-cx) > 0.001])
            cc = any([cc, abs(y-cy) > 0.001])
            return cc

    def setPos(self, digit=1, x=0, y=0):
        self.redrawView(digit, x, y)

    def getLoc(self, encode=True):

        if encode:
            x, y, i = self.getPos()
            x, y, i = str(x), str(y), str(i)
            return ':'.join([x, y, i])
