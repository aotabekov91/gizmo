from PyQt5 import QtCore

from .render import Part, Render

class Tile(Render):

    def setup(self):

        v=self.kwargs
        self.m_tiles=[]
        self.useTiling=v.get(
                'useTiling', False)
        super().setup()
        self.setTiles()

    def setTiles(self):

        if not self.useTiling: 
            tile=Part(self)
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
