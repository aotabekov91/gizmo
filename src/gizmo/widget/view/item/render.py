from math import floor
from PyQt5 import QtCore, QtGui

class RenderMixin:

    cropRectChanged = QtCore.pyqtSignal()
    linkClicked = QtCore.pyqtSignal(
            bool, int, float, float)
    painted=QtCore.pyqtSignal(
            object, object, object, object)

    def setRotation(self, rotation):
        self.rotation=rotation

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

    def paint(self, p, opts, wids):

        qpa=QtGui.QPainter.Antialiasing
        qpt=QtGui.QPainter.TextAntialiasing
        qps=QtGui.QPainter.SmoothPixmapTransform
        p.setRenderHints(qpa | qpt | qps)
        self.paintItem(p, opts, wids)
        self.painted.emit(p, opts, wids, self)

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

    def mapToElement(self, p, unify=True):

        t=self.m_trans.inverted()
        n=self.m_norm.inverted()
        if type(p) in [QtCore.QPoint, QtCore.QPointF]:
            uni=n[0].map(p)
            ununi=t[0].map(p)
        else:
            p=p.normalized()
            uni=n[0].mapRect(p)
            ununi=t[0].mapRect(p)
        if unify:
            return uni
        else:
            return ununi

    def mapToItem(self, p, isUnified=False):

        t=self.m_trans
        n=self.m_norm
        if type(p) in [QtCore.QPoint, QtCore.QPointF]:
            if isUnified: p=n.map(p)
            return t.map(p)
        else:
            p=p.normalized()
            if isUnified: p=n.mapRect(p)
            return t.mapRect(p)

    def setProxyGeometry(self, pos, proxy):

        width=proxy.preferredWidth()
        height=proxy.preferredHeight()
        x=pos.x()-0.5*proxy.preferredWidth()
        y=pos.y()-0.5*proxy.preferredHeight()
        proxyPadding=self.proxyPadding
        x=max([x, self.m_brect.left()+proxyPadding])
        y=max([y, self.m_brect.top()+ proxyPadding])
        width=min([width, self.m_brect.right()-proxyPadding-x])
        height=min([height, self.m_brect.bottom()-y])
        proxy.setGeometry(
                QtCore.QRectF(x, y, width, height))
