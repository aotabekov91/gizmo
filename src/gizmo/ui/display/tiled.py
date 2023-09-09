from PyQt6 import QtWidgets, QtCore

from gizmo.widget.layout import TileLayout

from .base import BaseDisplay

class TiledDisplay(BaseDisplay, QtWidgets.QWidget):

    def __init__(self, 
                 app,
                 window,
                 view_class=None,
                 objectName='Display',
                 ):

        super().__init__(parent=window)
        self.setup(app, window, view_class)
        window.resized.connect(
                self.m_layout.update)

    def setUI(self):

        self.setContentsMargins(0,0,0,0)
        self.setContextMenuPolicy(
                QtCore.Qt.NoContextMenu)
        self.m_layout = TileLayout(self)

    def clear(self):

        self.m_layout.clear()
        self.hide()

    def closeView(self, view=None, vid=None):

        if not view:
            view=self.currentView()
        if not vid and view:
            vid=view.id()
        for w in range(self.m_layout.root.widgets()):
            if w.id()==vid:
                self.m_layout.focusWidget(w)
                cw=self.m_layout.focusPrevious()
                self.m_layout.removeWidget(w)
                self.setCurrentView(cw)
                self.focusCurrent()

    def setView(self, 
                view, 
                how=None, 
                focus=True, 
                **kwargs):

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
        if focus: self.focusView(view)

    def focusView(self, view):

        self.setCurrentView(view)
        self.m_layout.focusWidget(view)

    def addWidget(self, widget, hsplit=False):

        self.m_layout.addWidget(widget, hsplit)

    def equalize(self): self.m_layout.equalize()

    def toggleSplit(self): self.m_layout.toggleSplit()

    def removeWidget(self):

        if self.m_layout.current:
            widget=self.m_layout.current.widget
            if widget: 
                self.focusPrevious()
                self.m_layout.removeWidget(widget)

    def focus(self, kind):

        node = self.m_layout.focus(kind)
        if node:
            self.setCurrentView(node.widget)
        return node

    def move(self, kind):

        return self.m_layout.move(kind)

    def flip(self, kind):

        return self.m_layout.flip(kind)

    def resize(self, direction, kind):

        return self.m_layout.resize(direction, kind)

    def split(self, hsplit=False): 

        if self.view: 
            model=self.view.model()
            self.open(model, how=None, hsplit=hsplit)
