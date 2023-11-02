from PyQt5 import QtWidgets, QtCore, QtGui

class XYMixin:

    def getPosition(self):

        if self.m_curr:
            i=self.m_items[self.m_curr]
            r=i.boundingRect().translated(i.pos())
            tl=self.viewport().rect().topLeft()
            tl=self.mapToScene(tl)
            x=(tl.x() -r.x())/r.width()
            y=(tl.y() -r.y())/r.height()
            return self.m_curr, x, y
        return 1, 0, 0

    def getLocation(self, encode=True):

        if encode:
            x, y, i = self.getPosition()
            x, y, i = str(x), str(y), str(i)
            return ':'.join([x, y, i])

    def isDifferentPos(
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
