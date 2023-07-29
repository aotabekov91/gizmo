from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class StackWidget(QStackedWidget):

    hideWanted=pyqtSignal()
    showWanted=pyqtSignal()

    resizeEventOccurred=pyqtSignal()

    focusLost=pyqtSignal()
    focusGained=pyqtSignal()

    def __init__ (self):

        super(StackWidget, self).__init__()

        self.main=None
        self.current=None
        self.previous=None
        self.centered=False

        self.listener=None

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setCentered(self, cond=False): self.centered=cond

    def installEventFilter(self, listener):

        self.listener=listener
        super().installEventFilter(listener)
        for i in range(self.count()): self.widget(i).installEventFilter(listener)

    def setFixedWidth(self, width):

        print(width)
        super().setFixedWidth(width)
        for i in range(self.count()): self.widget(i).setFixedWidth(width)

    def setFixedHeight(self, height):

        super().setFixedHeight(height)
        for i in range(self.count()): self.widget(i).setFixedHeight(height)

    def setFixedSize(self, size):

        super().setFixedSize(size)
        for i in range(self.count()): self.widget(i).setFixedSize(size)

    def addWidget(self, widget, name, main=False):

        widget.sid=super().addWidget(widget)
        setattr(self, name, widget)
        if main: self.main=widget
        if hasattr(widget, 'hideWanted'):
            widget.hideWanted.connect(self.hide)
            widget.hideWanted.connect(self.hideWanted)
        if hasattr(widget, 'showWanted'):
            widget.showWanted.connect(self.showWanted)
        if self.listener: widget.installEventFilter(self.listener)
        return widget.sid

    def removeWidget(self, widget):

        setattr(self, widget.name, None)
        if self.main==widget: setattr(self, 'main', None)
        if hasattr(widget, 'hideWanted'):
            widget.hideWanted.disconnect(self.hide)
            widget.hideWanted.disconnect(self.hideWanted)
        if hasattr(widget, 'showWanted'):
            widget.showWanted.disconnect(self.showWanted)
        if self.listener: widget.removeEventFilter(self.listener)
        widget.sid=None

    def show(self, widget=None, focus=True):

        super().show()

        if not widget: widget=self.main
        if widget:
            if self.current!=widget:
                self.previous=self.current
                if not self.previous: self.previous=self.current
                self.current=widget
            self.setCurrentIndex(widget.sid)
            self.current.show()
            if focus: self.setFocus()

        if self.centered: self.setLocation('center')
        self.showWanted.emit()

    def setFocus(self):

        super().setFocus()
        if self.current: self.current.setFocus()

    def event(self, event):

        if event.type()==QEvent.Enter: 
            self.setFocus()
        elif event.type()==QEvent.Resize:
            self.resizeEventOccurred.emit()
        return super().event(event)

    def adjustSize(self):
        
        super().adjustSize()
        for i in range(self.count()): self.widget(i).adjustSize()

    def setLocation(self, kind='center'):

        if kind=='center':
            frame=self.frameGeometry()
            desktop_center=QDesktopWidget().availableGeometry().center()
            frame.moveCenter(desktop_center)
            point=frame.topLeft()
            point.setY(150)
            self.move(point)

    def hide(self):

        super().hide()
        if self.centered: self.setLocation('center')
