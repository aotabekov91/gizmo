from math import floor
from PyQt5 import QtCore, QtGui, QtWidgets

from .base import Item

class RenderItem(Item, QtWidgets.QGraphicsObject):

    wasModified = QtCore.pyqtSignal()
    cropRectChanged = QtCore.pyqtSignal()
    linkClicked = QtCore.pyqtSignal(
            bool, int, float, float)
    painted=QtCore.pyqtSignal(
            object, object, object, object)

    def __init__(
            self, 
            *args,
            cache={},
            xresol=72,
            yresol=72,
            rotation=0,
            useTiling=False,
            devicePixelRatio=1.,
            **kwargs
            ):

        self.m_searched=[]
        self.m_cache=cache
        self.m_paint_links=False
        self.select_pcolor=QtCore.Qt.red
        self.m_brect = QtCore.QRectF() 
        self.m_trans = QtGui.QTransform()
        self.m_norm = QtGui.QTransform()
        self.xresol=xresol
        self.yresol=yresol
        self.rotation=rotation
        self.useTiling=useTiling
        self.devicePixelRatio=devicePixelRatio
        self.select_bcolor=QtGui.QColor(
                88, 139, 174, 30)
        super().__init__(
                *args, **kwargs)

    def setup(self):

        super().setup()
        self.setAcceptHoverEvents(True)
        self.updateSize()
        self.setCache()

    def setCache(self):

        v=self.m_view
        if v and hasattr(v, 'm_cache'):
            self.m_cache=self.m_view.m_cache

    def updateSize(self):

        if self.m_element:
            self.m_size = self.m_element.size()

    def paintItem(self, p, opts, wids):
        pass

    def setRotation(self, rotation):
        self.rotation=rotation

    def size(self): 
        return self.m_size

    def setXResol(self, xresol):
        self.xresol=xresol

    def setYResol(self, yresol):
        self.yresol=yresol

    def setSearched(self, searched=[]): 
        self.m_searched=searched

    def boundingRect(self):

        self.prepareGeometry()
        return self.m_brect

    def setupPaint(self, p, opts, wids):
        self.paintItem(p, opts, wids)

    def displayedWidth(self):
        return (self.xresol/72.0)*self.m_size.width()

    def displayedHeight(self):
        return (self.yresol/72.0)*self.m_size.height()

    def refresh(self, dropCache=False):
        self.update()

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
        self.setupPaint(p, opts, wids)
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

    def showOverlay(
            self, 
            overlay, 
            hideOverlay, 
            elements, 
            selectedElement
            ):

        for e in elements:
            if not e in overlay:
                self.addProxy(overlay, hideOverlay, e)
            if e==selectedElement:
                overlay[e].widget().setFocus()

    def hideOverlay(
            self, 
            overlay, 
            deleteLater=False
            ):

        dover=Overlay()
        dover.swap(overlay)
        if not dover.isEmpty():
            for i in range(dover.constEnd()):
                if deleteLater: 
                    raise
            self.refresh()

    def addProxy(
            self, 
            pos, 
            wid, 
            hideOverlay
            ):

        p=QtWidgets.QGraphicsProxyWidget(self)
        p.setWidget(wid)
        wid.setFocus()
        p.setAutoFillBackground(True)
        self.setProxyGeometry(pos, p)
        p.visibleChanged.connect(hideOverlay)

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
