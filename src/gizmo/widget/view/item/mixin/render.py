from math import floor
from PyQt5 import QtCore, QtGui

class RenderMixin:

    painted=QtCore.pyqtSignal(
            object, object, object, object)

    def boundingRect(self):

        self.prepareGeometry()
        return self.m_brect

    def refresh(self, dropCache=False):
        self.update()

    def size(self): 

        if self.m_element:
            self.m_size=self.m_element.size()
        return self.m_size

    def scaledResol(self): 

        s=self.scale
        r=self.devicePixelRatio
        x=self.xresol*s*r
        y=self.yresol*s*r
        return x, y

    def displayedSize(self):

        s=self.m_size
        w, h = None, None
        if s:
            w=(self.xresol/72.0)*s.width()
            h=(self.yresol/72.0)*s.height()
        return w, h

    def setResol(self, x, y):

        if self.xresol != x or self.yresol != y:
            if y>0 and x>0:
                # self.refresh()
                self.xresol=x
                self.yresol=y
                # self.redraw()

    # def redraw(self, refresh=False):
    #     if refresh: 
    #         self.refresh()
    #     self.prepareGeometryChange()
    #     self.prepareGeometry()

    def updateTrans(self):

        s = self.size()
        x = self.xresol*self.scale/72.
        y = self.yresol*self.scale/72.
        self.m_norm.reset()
        self.m_trans.reset()
        self.m_trans.scale(x, y)
        self.m_norm.scale(s.width(), s.height())

    def prepareGeometry(self):

        self.updateTrans()
        p=QtCore.QPointF()
        r=QtCore.QRectF(p, self.size())
        r=self.m_trans.mapRect(r)
        r.setWidth(floor(r.width()))
        r.setHeight(floor(r.height()))
        self.m_brect=r

    def paintItem(self, p, o, w):

        if self.m_element:
            r=self.rotation
            rect=self.m_brect
            x,y=self.scaledResol()
            img=self.m_element.render(
                    x, y, r, rect)
            img.setDevicePixelRatio(
                    self.devicePixelRatio)
            pmap=QtGui.QPixmap.fromImage(img)
            tl=self.m_brect.topLeft().toPoint()
            p.drawPixmap(tl, pmap)
            self.update()

    def paint(self, p, o, w):

        qpa=QtGui.QPainter.Antialiasing
        qpt=QtGui.QPainter.TextAntialiasing
        qps=QtGui.QPainter.SmoothPixmapTransform
        p.setRenderHints(qpa | qpt | qps)
        self.paintItem(p, o, w)
        self.painted.emit(p, o, w, self)
