from PyQt5 import QtCore

class Fit:

    canFit=True
    zoomMode=None
    zoomModeChanged=QtCore.pyqtSignal(
            object, object)

    def fitToWidth(self):
        self.setFitMode('width')

    def fitToHeight(self):
        self.setFitMode('height')

    def toggleFitMode(self):

        if self.zoomMode=='width':
            self.fitToHeight()
        else:
            self.fitToWidth()

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
