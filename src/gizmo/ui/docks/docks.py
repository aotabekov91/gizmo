from PyQt5 import QtCore, QtWidgets

from .dock import Dock

class Docks(QtCore.QObject):

    def __init__(self, window):

        super(Docks, self).__init__(
                parent=window)
        self.docks=[]
        self.current=None
        self.m_window=window
        self.fullscreen=False
        self.createDocks()

    def createDocks(self):

        self.m_window.setCorner(
                QtCore.Qt.TopLeftCorner, 
                QtCore.Qt.LeftDockWidgetArea)
        self.m_window.setCorner(
                QtCore.Qt.TopRightCorner, 
                QtCore.Qt.RightDockWidgetArea)
        self.m_window.setCorner(
                QtCore.Qt.BottomLeftCorner, 
                QtCore.Qt.LeftDockWidgetArea)
        self.m_window.setCorner(
                QtCore.Qt.BottomRightCorner, 
                QtCore.Qt.RightDockWidgetArea)
        locs = {
                'up': QtCore.Qt.TopDockWidgetArea,
                'down': QtCore.Qt.BottomDockWidgetArea,
                'left': QtCore.Qt.LeftDockWidgetArea,
                'right': QtCore.Qt.RightDockWidgetArea,
                }

        for loc, r in locs.items():
            d = Dock(loc)
            d.title=QtWidgets.QWidget()
            d.setTitleBarWidget(d.title)
            self.m_window.addDockWidget(r, d)
            setattr(self, f'{loc}', d)
            d.focusGained.connect(
                    self.setCurrent)
            self.docks+=[d]
        self.hideAll()

    def setTab(self, w, loc): 

        d=getattr(self, loc, None)
        if d: 
            self.delTab(w)
            d.setTab(w) 
        return d

    def delTab(self, w): 

        d=getattr(w, 'dock', None)
        if d: d.delTab(w)

    def hideAll(self):

        for d in self.docks: 
            d.hide()
            if d.current:
                m=getattr(d.current, 'mode', None)
                if m: m.deactivate()

    def move(self, loc, dock=None):

        d = dock or self.current
        if d and d.current:
            n=self.setTab(
                    d.current, loc)
            if n: 
                n.showWidget(n.current)

    def goto(self, loc):

        d=getattr(self, loc, None)
        if d and d.current:
            m=getattr(d.current, 'mode', None)
            if m: m.activate()

    def zoomIn(self, digit=1, dock=None): 

        d=dock or self.current
        if d: d.zoomIn(digit)

    def zoomOut(self, digit=1, dock=None): 

        d=dock or self.current
        if d: d.zoomOut(digit)

    def toggleFullscreen(self, dock=None):

        d = dock or self.current
        if d: d.toggleFullscreen()

    def setCurrent(self, dock):
        self.current=dock
