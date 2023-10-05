from PyQt5 import QtWidgets, QtCore

class Dock(QtWidgets.QDockWidget):

    def __init__(self, 
                 docks, 
                 loc,
                 objectName='DockWidget',
                 ):

        super().__init__(
                objectName=objectName)

        self.loc=loc
        self.name=loc
        self.widgets=[]
        self.docks=docks

        self.createTab()
        self.setContentsMargins(0, 0, 0, 0)

    def createTab(self):

        self.tab = QtWidgets.QStackedWidget(self)
        self.tab.setContentsMargins(0,0,0,0)
        self.setWidget(self.tab)

    def setFocus(self, widget=None):

        super().setFocus()

        if not widget: 
            widget=self.current()
        if widget:
            self.docks.setCurrent(self)
            self.show()
            self.tab.setCurrentIndex(
                    widget.index)
            self.tab.show()
            widget.setFocus()
            widget.focusGained.emit(widget)

    def activate(self, widget): 

        if not self.widgets or self.widgets[-1]!=widget: 
            self.widgets+=[widget]

        self.setFocus(widget)
        widget.show()
        widget.setFixedSize(self.tab.size())
        widget.prev_size=self.tab.size()
        widget.adjustSize()
        widget.dock.show()
        widget.dock.tab.show()
        widget.setFocus()
        widget.focusGained.emit(widget)

        self.docks.adjustDocks()

    def deactivate(self, widget, restore=False):

        if widget in self.widgets: 
            self.widgets.pop(self.widgets.index(widget))
        if restore and self.widgets:
            prev=self.widgets[-1]
            widget.dock.tab.setCurrentIndex(prev.index)
            self.activate(prev)
        else:
            self.hide()
            self.docks.adjustDocks()
            self.parent().main.setFocus()
        self.docks.adjustDocks()

    def event(self, event):

        if event.type()==QtCore.QEvent.Enter:
            current=self.current()
            if current: 
                current.focusGained.emit(current)
        if event.type()==QtCore.QEvent.Leave:
            current=self.current()
            if current: 
                current.focusLost.emit()
        return super().event(event)

    def current(self):

        if self.widgets: 
            return self.widgets[-1]

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.tab.installEventFilter(listener)

    def resize(self, 
               factor=1.2, 
               widget=None, 
               fullscreen=False, 
               restore=False):

        if not widget: widget=self.current()

        if widget:
            if fullscreen:
                widget.prev_size=widget.dock.tab.size()
                self.parent().main.hide()
                widget.dock.tab.setFixedSize(
                        self.parent().size())
                widget.setFixedSize(self.parent().size())
            elif restore:
                self.parent().main.show()
                widget.dock.tab.setFixedSize(
                        widget.prev_size)
                widget.setFixedSize(widget.prev_size)
            else:
                w=widget.prev_size.width()
                h=widget.prev_size.height()
                if self.loc in ['left', 'right']:
                    size=QtCore.QSize(round(w*factor), h)
                else:
                    size=QtCore.QSize(w, round(h*factor))
                widget.dock.tab.setFixedSize(size)
                widget.setFixedSize(size)
                widget.prev_size=widget.dock.tab.size()
