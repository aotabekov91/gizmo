from PyQt5 import QtCore

from gizmo.ui.display import BaseDisplay
from gizmo.widget.layout import TileLayout

class TiledDisplay(BaseDisplay):

    canGo=True
    canMove=True
    canSplit=True
    canFullscreen=True

    def setupUI(self):

        self.setContentsMargins(
                0,0,0,0)
        self.setContextMenuPolicy(
                QtCore.Qt.NoContextMenu)
        self.m_layout = TileLayout(self)

    def clear(self):

        self.hide()
        self.m_layout.clear()

    def closeView(
            self, 
            view=None, 
            vid=None
            ):

        if not view:
            view=self.m_curr
        if not vid and view:
            vid=view.id()
        l=self.m_layout
        for w in l.root.widgets():
            if w.view.id()==vid:
                l.focusWidget(w)
                p=l.focus('prev')
                if p:
                    l.removeWidget(w)
                    self.setCurrentView(
                            p.widget)
                return w

    def setView(
            self, 
            view, 
            how=None, 
            **kwargs
            ):

        self.setCurrentView(view)
        if how=='reset': self.clear()
        self.addWidget(view, **kwargs)
        self.connectView(view)
        self.setCurrentView(view)
        self.show()
        view.show()

    def addWidget(
            self, 
            widget, 
            **kwargs,
            ):

        self.m_layout.addWidget(
                widget, **kwargs)

    def removeWidget(self):

        c=self.m_layout.current
        self.disconnectView(c.widget)
        if c and c.widget: 
            self.focusPrevious()
            self.m_layout.removeWidget(
                    c.widget)

    def toggleFullscreen(
            self, view=None, **kwargs):
        raise

    def goTo(
            self, 
            view=None, 
            kind=None, 
            digit=None
            ):

        n = self.m_layout.goto(kind, digit)
        if n: self.setCurrentView(n.widget)
        return n

    def move(
            self, 
            view=None, 
            kind=None
            ):

        return self.m_layout.move(kind)

    def flip(
            self, 
            view=None, 
            kind=None
            ):

        return self.m_layout.flip(kind)

    def resize(
            self, 
            view=None,
            direction=None, 
            kind=None
            ):

        return self.m_layout.resize(
                direction, kind)

    def split(
            self, 
            view=None, 
            kind='vertical'
            ):

        v=view or self.m_curr
        cond=v.check('canCopy')
        if cond and kind=='vertical':
            v.copy(how=None, horizontal=False)
        elif cond and kind=='horizontal':
            v.copy(how=None, horizontal=True)

    def equalize(self):
        self.m_layout.equalize()

    def toggleSplit(self): 
        self.m_layout.toggleSplit()

    def update(self):
        self.m_layout.update()
