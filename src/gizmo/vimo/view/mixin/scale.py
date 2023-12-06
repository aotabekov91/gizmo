from PyQt5 import QtCore

class Scale:

    canScale=True
    scaleMode=None
    zoomFactor = 0.1
    scaleModeChanged=QtCore.pyqtSignal(
            object, object)

    def setup(self):

        super().setup()
        self.stateWanted.connect(
                self.updateScaleState)

    def updateScaleState(self, n, v):

        if n=='scaleMode':
            self.updateFit()

    def updateFit(self):

        if self.scaleMode in ['width', 'height']:
            self.setFitMode(self.scaleMode)

    def setParent(self, p):

        if self.parent(): 
            self.reconnect('disconnect')
        super().setParent(p)
        if self.parent(): 
            self.reconnect()

    def reconnect(self, kind='connect'):

        p=self.parent()
        g=getattr(p, 'geometryChanged', None)
        if g: 
            c=getattr(g, kind)
            c(self.updateFit)

    def scale(self, kind, *args, **kwargs):

        if kind=='width':
            self.setFitMode('width')
        elif kind=='height':
            self.setFitMode('height')
        elif kind=='in':
            self.setZoom('in', *args, **kwargs)
        elif kind=='out':
            self.setZoom('out', *args, **kwargs)

    def setFitMode(self, mode):

        self.setState('scaleMode', mode)
        self.delState('currentZoomFactor')
        if hasattr(self, 'hasItems'):
            self.fitItemsView(mode)
        self.redraw()
        self.scaleModeChanged.emit(
                self, mode)

    def fitItemsView(self, mode):

        s=self.size()
        w, h = s.width(), s.height()
        if hasattr(self, 'hasLayout'):
            w=self.m_layout.width(w)
            h=self.m_layout.height(h)
        zf=1
        for j, i in self.getItems():
            dw, dh = i.displayedSize()
            if mode =='width':
                zf=w/dw
            else:
                zf=min([w/float(dw), h/float(dh)])
            i.setZoomFactor(zf)

    def setZoom(self, kind='out', digit=1):

        sf = self.zoomFactor
        if kind=='out':
            zf=(1.-sf)**digit
        elif kind=='in':
            zf=(1.+sf)**digit
        self.setZoomFactor(zf)
        self.scaleModeChanged.emit(
                self, self.scaleMode)

    def setZoomFactor(self, factor):

        self.setState('scaleMode', 'scale')
        self.setState('currentZoomFactor', factor)
        if hasattr(self, 'hasItems'):
            self.zoomItemsView(factor)
        self.redraw()

    def zoomItemsView(self, zfactor):

        for i in self.m_items.values(): 
            if hasattr(i, 'canZoom'):
                n_zf=zfactor*i.scale
                i.setZoomFactor(n_zf)
