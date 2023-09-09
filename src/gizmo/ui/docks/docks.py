from PyQt5 import QtCore, QtWidgets

from .dock import Dock
from ...utils import register
from ..configure import Configure

class Docks(QtCore.QObject):

    keyPressEventOccurred=QtCore.pyqtSignal(object)

    def __init__(self, window):

        super(Docks, self).__init__()#window)

        self.prev=None
        self.current=None
        self.fullscreen=False

        self.window=window
        self.window.installEventFilter(self)

        self.createDocks()

        self.configure=Configure(
                app=window.app, 
                name='Docks', 
                parent=self, 
                mode_keys={'command':'d', 'normal':'d'})

    def createDocks(self):

        self.window.setCorner(
                QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.window.setCorner(
                QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.window.setCorner(
                QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.window.setCorner(
                QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        locs = {
                'top': QtCore.Qt.TopDockWidgetArea,
                'bottom': QtCore.Qt.BottomDockWidgetArea,
                'left': QtCore.Qt.LeftDockWidgetArea,
                'right': QtCore.Qt.RightDockWidgetArea,
                }

        for loc, area in locs.items():

            dock = Dock(self, loc)
            dock.setTitleBarWidget(QtWidgets.QWidget())

            if loc in ['right', 'left']:
                dock.tab.setFixedWidth(300)
            elif loc in ['top', 'bottom']:
                dock.tab.setFixedHeight(300)

            self.window.addDockWidget(area, dock)
            setattr(self, f'{loc}', dock)

        self.hideAll()

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.Resize:
            self.adjustDocks()
            return True
        return False

    def focus(self, position): 

        getattr(self, f'{position}').setFocus()

    def resize(self, ratio): 

        if self.current: self.current.resize(ratio)

    def setTab(self, w, loc): 

        w.dock=getattr(self, f'{loc}')
        w.index=w.dock.tab.addWidget(w)

    def delTab(self, w): 

        if self.current==w.dock: self.current.hide()
        w.dock.tab.removeWidget(w)

    def toggleFullscreen(self, dock=None):

        if not dock: dock=self.current

        if dock:

            self.setCurrent(dock)

            if not self.fullscreen:
                self.fullscreen=True
                self.current.resize(fullscreen=True)
            else:
                self.fullscreen=False
                self.window.display.show()
                self.current.resize(restore=True)

            self.focus(self.current.loc)

    def adjustDocks(self): 

        width=self.window.size().width()

        if self.left.isVisible():
            width-=self.left.size().width()
        if self.right.isVisible():
            width-=self.right.size().width()

        for position in ['top', 'bottom']: 
            dock=getattr(self, f'{position}')
            if dock.isVisible():
                dock.tab.setFixedWidth(width-5)
                widget=dock.current()
                if widget: 
                    size=dock.tab.size()
                    widget.setFixedSize(size)
                    widget.adjustSize()

    def hideAll(self):

        for dock in ['right', 'top', 'bottom', 'left']:
            getattr(self, f'{dock}').hide()

    def setCurrent(self, dock):

        if self.current!=dock:
            self.prev=self.current
            self.current=dock

    def zoom(self, kind='in', digit=1): 

        if self.current:

            if kind=='in': 
                factor=1.1**digit
            else:
                factor=.9**digit
            self.current.resize(factor=factor)
            self.current.setFocus()

    @register('h', modes=['command', 'normal'])
    def focusLeftDock(self): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.focus('left')

    @register('l', modes=['command', 'normal'])
    def focusRightDock(self): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.focus('right')

    @register('k', modes=['command', 'normal'])
    def focusTopDock(self): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.focus('top')

    @register('j', modes=['command', 'normal'])
    def focusBottomDock(self): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.focus('bottom') 

    @register('f', modes=['command', 'normal'])
    def toggleDockFullscreen(self): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.toggleFullscreen()

    @register('zi', modes=['command', 'normal'])
    def zoomInDock(self, digit=1): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.zoom('in', digit)

    @register('zo', modes=['command', 'normal'])
    def zoomOutDock(self, digit=1): 

        self.window.app.plugman.plugs.command.delisten_wanted=None
        self.zoom('out', digit)
