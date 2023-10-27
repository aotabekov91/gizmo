from math import floor
from PyQt5 import QtCore, QtGui, QtWidgets

from .utils.tile import Tile

class Item(QtWidgets.QGraphicsObject):

    wasModified = QtCore.pyqtSignal()
    cropRectChanged = QtCore.pyqtSignal()
    linkClicked = QtCore.pyqtSignal(
            bool, int, float, float)
    itemPainted=QtCore.pyqtSignal(
            object, object, object, object)
    mouseDoubleClick=QtCore.pyqtSignal(
            int, object)
    mouseReleaseOccured=QtCore.pyqtSignal(
            object, object)
    mouseMoveOccured=QtCore.pyqtSignal(
            object, object)
    mousePressOccured=QtCore.pyqtSignal(
            object, object)
    hoverMoveOccured=QtCore.pyqtSignal(
            object, object)
    mouseDoubleClickOccured=QtCore.pyqtSignal(
            object, object)

    def __init__(
            self, 
            element, 
            view, 
            index=None,
            **kwargs
            ):

        self.m_view=view
        self.m_index=index
        self.m_searched=[]
        self.m_paint_links=False
        self.m_element = element
        self.m_cache=view.m_cache
        self.m_size = element.size()
        self.select_pcolor=QtCore.Qt.red
        self.m_brect = QtCore.QRectF() 
        self.m_transform = QtGui.QTransform()
        self.m_normalizedTransform = QtGui.QTransform()
        s=view.settings()
        self.m_rotation=s.get('rotation', 0)
        self.m_xresol=s.get('resolutionX', 72)
        self.m_yresol=s.get('resolutionY', 72)
        self.m_use_tiling=s.get('useTiling', False)
        self.m_scaleFactor=s.get('scaleFactor', 1.)
        self.m_proxy_padding=s.get('proxyPadding', 0.)
        self.m_device_pixel_ration=s.get(
                'devicePixelRatio', 1.)
        self.select_bcolor=QtGui.QColor(88, 139, 174, 30)
        super().__init__(objectName='Item', **kwargs)
        self.setAcceptHoverEvents(True)
        self.setup()

    def setup(self):
        pass

    def select(self, *args, **kwargs):
        pass

    def paintItem(self, p, opts, wids):
        pass

    def index(self):
        return self.m_index

    def setIndex(self, idx):
        self.m_index=idx

    def element(self): 
        return self.m_element

    def view(self): 
        return self.m_view

    def proxyPadding(self):
        return self.m_proxy_padding

    def scale(self):
        return self.m_scaleFactor

    def rotation(self):
        return self.m_rotation

    def setRotation(self, rotation):
        self.m_rotation=rotation

    def devicePixelRatio(self):
        return self.m_device_pixel_ration

    def size(self): 
        return self.m_size

    def xresol(self):
        return self.m_xresol 

    def setXResol(self, xresol):
        self.m_xresol=xresol

    def yresol(self):
        return self.m_yresol

    def setYResol(self, yresol):
        self.m_yresol=yresol

    def setSearched(self, searched=[]): 
        self.m_searched=searched

    def boundingRect(self):

        self.prepareGeometry()
        return self.m_brect

    def setupPaint(self, p, opts, wids):
        self.paintItem(p, opts, wids)

    def displayedWidth(self):
        return (self.xresol()/72.0)*self.m_size.width()

    def displayedHeight(self):
        return (self.yresol()/72.0)*self.m_size.height()

    def refresh(self, dropCache=False):
        self.update()

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickOccured.emit(self, event)

    def mousePressEvent(self, event):
        self.mousePressOccured.emit(self, event)

    def mouseMoveEvent(self, event):
        self.mouseMoveOccured.emit(self, event)

    def mouseReleaseEvent(self, event):
        self.mouseReleaseOccured.emit(self, event)

    def hoverMoveEvent(self, event):
        self.hoverMoveOccured.emit(event, self)


    def scaledResolutionX(self): 

        s=self.scale()
        r=self.devicePixelRatio()
        x=self.xresol()
        return s*r*x

    def scaledResolutionY(self): 

        s=self.scale()
        r=self.devicePixelRatio()
        y=self.yresol()
        return s*r*y

    def paint(self, p, opts, wids):

        qpa=QtGui.QPainter.Antialiasing
        qpt=QtGui.QPainter.TextAntialiasing
        qps=QtGui.QPainter.SmoothPixmapTransform
        p.setRenderHints(qpa | qpt | qps)
        self.setupPaint(p, opts, wids)
        self.itemPainted.emit(p, opts, wids, self)

    def setResolution(self, x, y):

        if self.xresol() != x or self.yresol() != y:
            if y>0 and x>0:
                self.refresh()
                self.setXResol(x)
                self.setYResol(y)
                self.redraw()

    def setScaleFactor(self, factor):

        self.m_scaleFactor=factor
        self.redraw(refresh=True)

    def redraw(self, refresh=False):

        if refresh: 
            self.refresh()
        self.prepareGeometryChange()
        self.prepareGeometry()

    def prepareGeometry(self):

        s = self.size()
        x = self.xresol()*self.scale()/72.
        y = self.yresol()*self.scale()/72.
        t=self.m_transform
        n=self.m_normalizedTransform
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

    def mapToPage(self, p, unify=True):

        t=self.m_transform.inverted()
        n=self.m_normalizedTransform.inverted()
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

        t=self.m_transform
        n=self.m_normalizedTransform
        if type(p) in [QtCore.QPoint, QtCore.QPointF]:
            if isUnified: p=n.map(p)
            return t.map(p)
        else:
            p=p.normalized()
            if isUnified: p=n.mapRect(p)
            return t.mapRect(p)

    def showOverlay(self, 
                    overlay, 
                    hideOverlay, 
                    elements, 
                    selectedElement):

        for e in elements:
            if not e in overlay:
                self.addProxy(overlay, hideOverlay, e)
            if e==selectedElement:
                overlay[e].widget().setFocus()

    def hideOverlay(self, overlay, deleteLater=False):

        dover=Overlay()
        dover.swap(overlay)
        if not dover.isEmpty():
            for i in range(dover.constEnd()):
                if deleteLater: 
                    raise
            self.refresh()

    def addProxy(self, pos, wid, hideOverlay):

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
        proxyPadding=self.proxyPadding()
        x=max([x, self.m_brect.left()+proxyPadding])
        y=max([y, self.m_brect.top()+ proxyPadding])
        width=min([width, self.m_brect.right()-proxyPadding-x])
        height=min([height, self.m_brect.bottom()-y])
        proxy.setGeometry(
                QtCore.QRectF(x, y, width, height))

    # def name(self): 
    #     idx=self.m_element.index()
    #     count=self.m_view.count()
    #     return f'{idx}/{count}'
