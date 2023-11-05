from math import floor, ceil
from PyQt5 import QtCore, QtGui

from .part import Part

class Render:

    canRender=True
    painted=QtCore.pyqtSignal(
            object, object, object, object)

    def setup(self):

        v=self.kwargs
        self.m_parts=[]
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
        self.tileSize=v.get(
                'tileSize', 1024)
        self.useTiling=v.get(
                'useTiling', False) # todo true bug
        self.setTiles()
        super().setup()

    def setTiles(self):

        self.m_parts=[]
        if not self.useTiling:
            self.m_parts=[Part(self)]
        self.redraw()

    def refresh(self, dropCache=False):

        for tile in self.m_parts:
            tile.refresh(dropCache)
            if dropCache: 
                tile.dropCaches(self)
        super().refresh(dropCache)

    def redraw(self, refresh=False):

        if refresh: self.update()
        self.prepareGeometryChange()
        self.prepareGeometry()

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

        tl=self.m_brect.topLeft()
        # self.m_tiles[0].paint(p, tl)
        e=o.exposedRect
        te = e.translated(-tl)
        for t in self.m_parts:
            r=QtCore.QRectF(t.rect())
            if te.intersects(r):
                t.paint(p, tl)
            else:
                t.cancelRender()

    def paint(self, p, o, w):

        qpa=QtGui.QPainter.Antialiasing
        qpt=QtGui.QPainter.TextAntialiasing
        qps=QtGui.QPainter.SmoothPixmapTransform
        p.setRenderHints(qpa | qpt | qps)
        self.paintItem(p, o, w)
        self.painted.emit(p, o, w, self)

    def startRender(self, prefetch):
        
        for tile in self.m_parts:
            tile.startRender(prefetch)

    def cancelRender(self):

        for tile in self.m_parts:
            tile.cancelRender()

    def prepareTiling(self):

        if not self.useTiling:
            r=self.m_brect
            w = int(r.width())
            h = int(r.height())
            r=QtCore.QRect(0, 0, w, h)
            self.m_parts[0].setRect(r)
        else:
            ts=self.tileSize
            pw = self.m_brect.width();
            ph = self.m_brect.height();
            tw, th = ts, ts
            if pw < ph: tw=ts * pw / ph
            if ph < pw: th=ts * ph / pw
            cc = ceil(pw / tw)
            rc = ceil(ph / th)
            tw = ceil(pw / cc);
            th = ceil(ph / rc);
            nc = cc * rc;
            oc = len(self.m_parts)
            for i in range(nc, oc):
                part=self.m_parts[i]
                part.deleteAfterRender()
            self.m_parts=self.m_parts[:nc]
            for i in range(oc, nc):
                if i<len(self.m_parts):
                    self.m_parts[i]=Part(self)
                else:
                    self.m_parts+=[Part(self)]
            if oc != nc:
                for t in self.m_parts:
                    t.dropObsoletePixmap()
            for c in range(0, cc):
                for r in range(0, rc):
                    l, t =0., 0.
                    w, h=pw-l, ph-t
                    if r>0: t=r*th
                    if c>0: l=c*tw
                    if c<(cc-1): w=tw
                    if r<(rc-1): h=th
                    p=self.m_parts[c * rc + r]
                    nr=QtCore.QRect(
                            int(l), int(t), int(w), int(h))
                    p.setRect(nr)

    def mapToPage(self, obj, unify=True):

        if type(obj) in [QtCore.QPoint, QtCore.QPointF]:
            ununified=self.m_transform.inverted()[0].map(obj)
            unified=self.m_normalizedTransform.inverted()[0].map(obj)
        else:
            polygon=obj.normalized()
            ununified=self.m_transform.inverted()[0].mapRect(polygon)
            unified=self.m_normalizedTransform.inverted()[0].mapRect(polygon)

        if unify:
            return unified
        else:
            return ununified

    def mapToItem(self, polygon, isUnified=False):

        if type(polygon) in [QPoint, QPointF]:
            if isUnified: polygon=self.m_normalizedTransform.map(polygon)
            return self.m_transform.map(polygon)
        else:
            polygon=polygon.normalized()
            if isUnified: polygon=self.m_normalizedTransform.mapRect(polygon)
            return self.m_transform.mapRect(polygon)
