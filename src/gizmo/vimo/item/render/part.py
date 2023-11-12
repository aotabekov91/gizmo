from PyQt5 import QtCore, QtGui

from .task import Task

class Part(QtCore.QObject):

    cropRectChanged = QtCore.pyqtSignal()

    def __init__(self, item):

        self.m_cache={}
        self.m_item=item
        self.m_error = False
        self.m_rect = QtCore.QRect()
        self.m_pixmap = QtGui.QPixmap()
        self.m_cropRect = QtCore.QRectF() 
        self.m_obsoletePixmap = QtGui.QPixmap()
        super().__init__(item)
        self.setup()

    def setup(self):

        self.m_runner = Task(self)
        self.m_runner.finished.connect(
            self.on_renderTask_finished)
        self.m_runner.imageReady.connect(
            self.on_renderTask_imageReady)
        self.m_runner.cancel(True)
        self.m_runner.wait()

    def on_renderTask_imageReady(
            self, rect, prefetch, img):

        if img is None:
            self.m_error=True
            return
        if self.m_rect==rect:
            self.m_obsoletePixmap=QtGui.QPixmap()
            c=self.m_runner.wasCanceled()
            f=self.m_runner.wasCanceledForcibly()
            if prefetch and not f:
                k=self.cacheKey()
                p=QtGui.QPixmap.fromImage(img)
                self.m_cache[k]=p
            elif not c: 
                pmap=QtGui.QPixmap.fromImage(img)
                self.m_pixmap=pmap

    def takePixmap(self):

        k = self.cacheKey()
        pmap = self.m_cache.get(k)

        if self.isNotEmptyPixmap(pmap):
            self.m_obsoletePixmap = QtGui.QPixmap() 
            return pmap
        elif self.isNotEmptyPixmap(self.m_pixmap):
            self.m_cache[k]=self.m_pixmap
            pmap = self.m_pixmap
            self.m_pixmap = QtGui.QPixmap() 
            return pmap
        else:
            self.startRender()

    def refresh(self, dropCache=False):

        if not dropCache:
            obj = self.m_cache.get(self.cacheKey())
            if obj :
                self.m_obsoletePixmap = obj
        else:
            self.m_cache={}
            # k=self.cacheKey()
            # if k in self.m_cache:
                # self.m_cache.pop(k)
            self.m_obsoletePixmap = QtGui.QPixmap() 
        self.m_error = False
        self.m_runner.cancel(True)
        self.m_pixmap =QtGui.QPixmap()

    def startRender(self, prefetch=False):

        if self.m_error:
            return
        elif self.m_runner.isRunning():
            return
        c=self.cacheKey() in self.m_cache
        if prefetch and c:
            return
        self.m_runner.start(
                self.m_rect, prefetch)

    def cancelRender(self):

        self.m_runner.cancel()
        self.m_pixmap=QtGui.QPixmap()
        self.m_obsoletePixmap=QtGui.QPixmap()

    def deleteAfterRender(self):

        self.cancelRender()
        if not self.m_runner.isRunning():
            del self

    def on_renderTask_finished(self):
        self.m_item.update()

    def cacheKey(self):

        s=self.m_rect
        i = self.m_item
        data = (
            i.xresol, i.yresol, i.scale,
            (s.x(), s.y(), s.width(), s.height()),
        )
        return (i, data)

    def rect(self):
        return self.m_rect

    def setRect(self, rect):
        self.m_rect = rect

    def dropPixmap(self):
        self.m_pixmap = None 

    def dropObsoletePixmap(self):
        self.m_obsoletePixmap = None 

    def dropCaches(self, page):

        items=self.m_cache.items()
        for k, m in list(items):
            if k[0]==page: 
                self.m_cache.pop(k)

    def paint(self, p, topLeft):

        pmap = self.takePixmap()
        if self.isNotEmptyPixmap(pmap):
            p.drawPixmap(
                    self.m_rect.topLeft()+topLeft, 
                    pmap)
        elif self.isNotEmptyPixmap(self.m_obsoletePixmap):
            # p=QtCore.QRectF(self.m_rect).translated(topLeft)
            r=QtCore.QRectF(self.m_rect).translated(topLeft)
            p.drawPixmap(
                    r,
                    self.m_obsoletePixmap, 
                    QtCore.QRectF())

    def isNotEmptyPixmap(self, pixmap):

        if pixmap is not None:
            if pixmap!=QtGui.QPixmap(): 
                size=pixmap.size()
                if size.width()*size.height()>0: 
                    return True
