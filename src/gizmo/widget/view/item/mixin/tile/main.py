from PyQt5 import QtCore, QtGui

from .tile import Tile

class TileMixin:

    def setup(self):

        super().setup()
        self.m_tiles=[]
        if not self.useTiling: 
            tile=Tile(self)
            self.m_tiles=[tile]
        self.redraw()

    def paintItem(self, p, o, w):

        if self.isVisible():
            tl=self.m_brect.topLeft()
            self.m_tiles[0].paint(p, tl)

    def prepareGeometry(self):

        super().prepareGeometry()
        self.prepareTiling()

    def prepareTiling(self):

        r=self.m_brect
        w, h=int(r.width()), int(r.height())
        r=QtCore.QRect(0, 0, w, h)
        self.m_tiles[0].setRect(r)

    def refresh(self, dropCache=False):

        for tile in self.m_tiles:
            tile.refresh(dropCache)
            if dropCache: 
                tile.dropCaches(self)
        super().refresh(dropCache)

    def startRender(self, prefetch):
        
        for tile in self.m_tiles:
            tile.startRender(prefetch)

    def cancelRender(self):

        for tile in self.m_tiles:
            tile.cancelRender()
