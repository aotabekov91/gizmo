from math import floor
from PyQt5 import QtCore, QtGui

from .part import Part

class Render:

    canRender=True
    painted=QtCore.pyqtSignal(
            object, object, object, object)

    def setup(self):

        v=self.kwargs
        super().setup()
        self.setTiles()

    def setTiles(self):

        self.m_tile=Part(self)
        self.redraw()

    def prepareTiling(self):

        r=self.m_brect
        w, h=int(r.width()), int(r.height())
        r=QtCore.QRect(0, 0, w, h)
        self.m_tile.setRect(r)

    def refresh(self, dropCache=False):

        self.m_tile.refresh(dropCache)
        if dropCache: 
            self.m_tile.dropCaches(self)
        super().refresh(dropCache)

    def startRender(self, prefetch):
        self.m_tile.startRender(prefetch)

    def cancelRender(self):
        self.m_tile.cancelRender()

    def redraw(self, refresh=False):

        if refresh: self.update()
        self.prepareGeometryChange()
        self.prepareGeometry()

    def setup(self):

        v=self.kwargs
        self.m_norm = QtGui.QTransform()
        self.m_trans = QtGui.QTransform()
        self.scale=v.get(
                'xresol', 1.)
        self.xresol=v.get(
                'xresol', 72.)
        self.yresol=v.get(
                'yresol', 72.)
        self.rotation=v.get(
                'rotation', 0)
        self.devicePixelRatio=v.get(
                'devicePixelRatio', 0)
        super().setup()

    def boundingRect(self):

        self.prepareGeometry()
        return self.m_brect

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

    def setResol(self, x, y):

        if y>0 and x>0:
            c1 = self.xresol != x
            c2 = self.yresol != y
            if c1 or c2:
                self.xresol=x
                self.yresol=y

    def displayedSize(self):

        s=self.m_size
        w, h = None, None
        if s:
            w=(self.xresol/72.0)*s.width()
            h=(self.yresol/72.0)*s.height()
        return w, h

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
        self.prepareTiling()

    # def paintItem(self, p, o, w):
    #     if self.m_element:
    #         r=self.rotation
    #         rect=self.m_brect
    #         x,y=self.scaledResol()
    #         img=self.m_element.render(
    #                 x, y, r, rect)
    #         img.setDevicePixelRatio(
    #                 self.devicePixelRatio)
    #         pmap=QtGui.QPixmap.fromImage(img)
    #         tl=self.m_brect.topLeft().toPoint()
    #         p.drawPixmap(tl, pmap)
    #         self.update()

    def paintItem(self, p, o, w):

        if self.isVisible():
            tl=self.m_brect.topLeft()
            self.m_tile.paint(p, tl)

    def paint(self, p, o, w):

        qpa=QtGui.QPainter.Antialiasing
        qpt=QtGui.QPainter.TextAntialiasing
        qps=QtGui.QPainter.SmoothPixmapTransform
        p.setRenderHints(qpa | qpt | qps)
        self.paintItem(p, o, w)
        self.painted.emit(p, o, w, self)

    def mapToElement(self, *args, **kwargs):
        raise

    def mapToItem(self, *args, **kwargs):
        raise
