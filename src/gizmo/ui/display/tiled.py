from PyQt5 import QtCore

from gizmo.ui.display import BaseDisplay
from gizmo.widget.layout import TileLayout

class TiledDisplay(BaseDisplay):

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
            focus=True, 
            **kwargs
            ):

        self.setCurrentView(view)
        if how=='reset':
            self.clear()
            self.m_layout.addWidget(view)
        elif how=='below':
            self.m_layout.addWidget(view)
        else:
            self.m_layout.addWidget(
                    view, **kwargs)
        self.show()
        view.show()
        if focus: 
            self.focusView(view)

    def focusView(self, view):

        self.setCurrentView(
                view)
        self.m_layout.focusWidget(
                view)

    def addWidget(
            self, 
            widget, 
            hsplit=False
            ):

        self.m_layout.addWidget(
                widget, hsplit)

    def removeWidget(self):

        c=self.m_layout.current
        if c and c.widget: 
            self.focusPrevious()
            self.m_layout.removeWidget(
                    c.widget)

    def toggleFullscreen(self):
        raise

    def goto(self, kind=None, digit=None):

        n = self.m_layout.goto(
                kind, digit)
        if n:
            w=n.widget
            self.setCurrentView(w)
        return n

    def move(self, kind):

        return self.m_layout.move(
                kind)

    def flip(self, kind):

        return self.m_layout.flip(
                kind)

    def resize(self, direction, kind):

        return self.m_layout.resize(
                direction, kind)

    def split(self, hsplit=False): 

        copy=self.copyView(self.m_curr)
        if copy:
            r, v = copy
            r.setView(
                    view=v,
                    how=None,
                    hsplit=hsplit)

    def equalize(self):
        self.m_layout.equalize()

    def toggleSplit(self): 
        self.m_layout.toggleSplit()

    def update(self):
        self.m_layout.update()
