from PyQt5 import QtCore

class Scale:

    canScale=True
    scaleMode=None
    zoomFactor = 0.1
    scaleModeChanged=QtCore.pyqtSignal(
            object, object)

    def scale(self, kind, *args, **kwargs):

        if kind=='fitToWidth':
            self.setFitMode('width')
        elif kind=='fitToHeight':
            self.setFitMode('height')
        elif kind=='zoomIn':
            self.setZoom('in', *args, **kwargs)
        elif kind=='zoomOut':
            self.setZoom('out', *args, **kwargs)

    def setFitMode(self, mode):

        self.scaleMode=mode
        if hasattr(self, 'hasItems'):
            self.fitItemsView(mode)
        self.redraw()
        self.scaleModeChanged.emit(
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

    def setZoom(self, kind='out', digit=1):

        self.scaleMode='scale'
        sf = self.zoomFactor
        if kind=='out':
            zf=(1.-sf)**digit
        elif kind=='in':
            zf=(1.+sf)**digit
        self.setZoomFactor(zf)
        self.scaleModeChanged.emit(
                self, self.scaleMode)

    def setZoomFactor(self, zfactor):

        if hasattr(self, 'hasItems'):
            self.zoomItemsView(zfactor)
        self.redraw()

    def zoomItemsView(self, zfactor):

        for i in self.m_items.values(): 
            if hasattr(i, 'canZoom'):
                n_zf=zfactor*i.scale
                i.setZoomFactor(n_zf)
