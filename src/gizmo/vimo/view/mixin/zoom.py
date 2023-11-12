from PyQt5 import QtCore

class Zoom:

    canZoom=True
    zoomMode=None
    zoomFactor = 0.1
    zoomModeChanged=QtCore.pyqtSignal(
            object, object)

    def fitToWidth(self):
        self.setFitMode('width')

    def fitToHeight(self):
        self.setFitMode('height')

    def setFitMode(self, mode):

        self.zoomMode=mode
        if hasattr(self, 'hasItems'):
            self.fitItemsView(mode)
        self.redraw()
        self.zoomModeChanged.emit(
                self, mode)

    def fitItemsView(self, mode):

        s=self.size()
        w, h = s.width(), s.height()
        if hasattr(self, 'hasLayout'):
            w=self.m_layout.width(h)
            h=self.m_layout.height(h)
        for j, i in self.getItems():
            dw, dh = i.displayedSize()
            if mode =='width':
                s=w/dw
            else:
                s=min([w/float(dw), h/float(dh)])
            i.setZoomFactor(s)

    def zoomIn(self, digit=1):
        self.setZoom('in', digit)

    def zoomOut(self, digit=1): 
        self.setZoom('out', digit)
        
    def setZoom(self, kind='out', digit=1):

        self.zoomMode='scale'
        zf = self.zoomFactor
        if kind=='out':
            zf=(1.-zf)**digit
        elif kind=='in':
            zf=(1.+zf)**digit
        self.setZoomFactor(zf)
        self.zoomModeChanged.emit(
                self, self.zoomMode)

    def setZoomFactor(self, zfactor):

        self.savePosition()
        if hasattr(self, 'hasItems'):
            self.zoomItemsView(zfactor)
        self.redraw()
        self.setPosition()

    def zoomItemsView(self, zfactor):

        for i in self.m_items.values(): 
            if hasattr(i, 'canZoom'):
                n_zf=zfactor*i.scale
                i.setZoomFactor(n_zf)

    def savePosition(self):

        self.pos=None
        if hasattr(self, 'canPosition'):
            self.pos=self.getPosition()

    def setPosition(self):

        if self.pos:
            self.goto(*self.pos)
