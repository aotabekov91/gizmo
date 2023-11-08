from PyQt5 import QtWidgets, QtCore, QtGui

from .base import Position

class XYPos(Position):

    def getPosition(self):

        if self.m_curr and self.m_items:
            i=self.m_items[self.m_curr]
            r=i.boundingRect().translated(i.pos())
            tl=self.viewport().rect().topLeft()
            tl=self.mapToScene(tl)
            x=(tl.x() -r.x())/r.width()
            y=(tl.y() -r.y())/r.height()
            return self.m_curr, x, y
        return 1, 0, 0

    def getLocation(self):

        i, x, y = self.getPosition()
        i = str(i)[:3]
        x = str(x)[:3]
        y = str(y)[:3]
        return ':'.join([i, x, y])

    def parseLocation(self, loc):

        if loc:
            t=loc.split(':')
            if len(t)==3:
                i=int(t[0])
                x=float(t[1])
                y=float(t[2])
                return i, x, y

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

    def gotoFirst(self):
        self.goto(1)

    def gotoLast(self):
        self.goto(self.count())

    def goto(self, digit=1, x=0, y=0):

        self.redrawView(digit, x, y)
        self.setVisibleItem()
