from math import floor
from PyQt5 import QtCore, QtGui

class RenderMixin:

    cropRectChanged = QtCore.pyqtSignal()
    painted=QtCore.pyqtSignal(
            object, object, object, object)

    def setXResol(self, xresol):
        self.xresol=xresol

    def setYResol(self, yresol):
        self.yresol=yresol

    def boundingRect(self):

        self.prepareGeometry()
        return self.m_brect

    def displayedWidth(self):
        return (self.xresol/72.0)*self.m_size.width()

    def displayedHeight(self):
        return (self.yresol/72.0)*self.m_size.height()

    def refresh(self, dropCache=False):
        self.update()

    def size(self): 

        if self.m_element:
            self.m_size=self.m_element.size()
        return self.m_size

    def scaledResol(self, kind): 

        s=self.scale
        r=self.devicePixelRatio
        if kind=='x':
            return self.xresol*s*r
        elif kind=='y':
            return self.yresol*s*r

    def paintItem(self, p, o, w):

        if self.m_element:
            self.m_element.render()

    def paint(self, p, o, w):

        qpa=QtGui.QPainter.Antialiasing
        qpt=QtGui.QPainter.TextAntialiasing
        qps=QtGui.QPainter.SmoothPixmapTransform
        p.setRenderHints(qpa | qpt | qps)
        self.paintItem(p, o, w)
        self.painted.emit(p, o, w, self)

    def setResol(self, x, y):

        if self.xresol != x or self.yresol != y:
            if y>0 and x>0:
                self.refresh()
                self.setXResol(x)
                self.setYResol(y)
                self.redraw()

    def redraw(self, refresh=False):

        if refresh: 
            self.refresh()
        self.prepareGeometryChange()
        self.prepareGeometry()

    def prepareGeometry(self):

        s = self.size()
        t, n=self.m_trans, self.m_norm
        x = self.xresol*self.scale/72.
        y = self.yresol*self.scale/72.
        t.reset()
        t.scale(x, y)
        n.reset()
        n.scale(s.width(), s.height())
        br=QtCore.QRectF(QtCore.QPointF(), s)
        self.m_brect=t.mapRect(br)
        w=floor(self.m_brect.width())
        h=floor(self.m_brect.height())
        self.m_brect.setWidth(w)
        self.m_brect.setHeight(h)
