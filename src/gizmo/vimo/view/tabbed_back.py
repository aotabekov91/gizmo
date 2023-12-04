from PyQt5 import QtWidgets, QtCore

class Dock(QtWidgets.QDockWidget):

    focusGained=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            loc=None, 
            min_width=200,
            min_height=200,
            zoom_factor=0.1,
            objectName='DockWidget',
            **kwargs):

        super().__init__(
                objectName=objectName)

        self.loc=loc
        self.current=None
        self.fullscreen=None
        self.min_w=min_width
        self.min_h=min_height
        self.zfactor=zoom_factor
        self.createTab()

    def createTab(self):

        t = QtWidgets.QStackedWidget(self)
        self.setWidget(t)
        self.tab = t 

    def setTab(self, w):

        w.idx=self.tab.addWidget(w)
        w.setMinimumSize(
                self.min_w, self.min_h)
        w.position=self.loc
        w.dock=self
        w.isDockView=True
        self.current=w

    def delTab(self, w):

        self.tab.removeWidget(w)
        self.deactivate()
        delattr(w, 'isDockView')
        w.dock=None

    def showWidget(self, w):

        idx=w.idx
        self.show()
        self.tab.show()
        self.tab.setCurrentIndex(idx)
        w.setFocus()
        w.show()

    def toggleFullscreen(self):

        w=self.current
        p=self.parent()
        if not self.fullscreen:
            self.fullscreen=w.size()
            w.setFixedSize(p.size())
        else:
            w.setFixedSize(self.fullscreen)
            self.fullscreen=None

    def scale(self, kind, digit=1):

        if self.current:
            self.setZoom(kind, digit)

    def setZoom(self, kind, digit=1):

        if kind=='out':
            zf=(1.-self.zfactor)**digit
        elif kind=='in':
            zf=(1.+self.zfactor)**digit
        else: 
            return
        s=self.size()
        w, h = s.width(), s.height()
        c=self.current.size()
        if self.loc in ['left', 'right']:
            w=int(c.width()*zf)
            self.current.setFixedWidth(w)
        else:
            h=int(c.height()*zf)
            self.current.setFixedHeight(h)

    def activate(self, w):

        self.setFocus()
        self.current=w
        self.showWidget(w)
        self.focusGained.emit(self)

    def deactivate(self, widget=None):
        self.hide()
