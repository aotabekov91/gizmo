from PyQt5 import QtWidgets, QtCore, QtGui

class BaseDisplay:

    viewCreated=QtCore.pyqtSignal(object)
    viewChanged=QtCore.pyqtSignal(object)

    itemChanged = QtCore.pyqtSignal(object, object)
    itemPainted = QtCore.pyqtSignal(
            object, object, object, object, object)
    positionChanged = QtCore.pyqtSignal(
            object, object, object, object)

    itemKeyPressOccured=QtCore.pyqtSignal(
            [object, object, object])
    itemHoverMoveOccured=QtCore.pyqtSignal(
            [object, object, object])
    itemMouseMoveOccured=QtCore.pyqtSignal(
            [object, object, object])
    itemMousePressOccured=QtCore.pyqtSignal(
            [object, object, object])
    itemMouseReleaseOccured=QtCore.pyqtSignal(
            [object, object, object])
    itemMouseDoubleClickOccured=QtCore.pyqtSignal(
            [object, object, object])

    viewSelection=QtCore.pyqtSignal(
            [object, object])
    viewKeyPressOccurred=QtCore.pyqtSignal(
            [object, object])
    viewHoverMoveOccured=QtCore.pyqtSignal(
            [object, object])
    viewMouseMoveOccured=QtCore.pyqtSignal(
            [object, object])
    viewMousePressOccured=QtCore.pyqtSignal(
            [object, object])
    viewMouseReleaseOccured=QtCore.pyqtSignal(
            [object, object])
    viewMouseDoubleClickOccured=QtCore.pyqtSignal(
            [object, object])

    def __init__(self, 
            app, 
            window, 
            view_class=None):

        super().__init__(parent=window)
        self.app=app
        self.win=window
        self.view_class=view_class
        self.count=-1
        self.views={}
        self.view=None
        self.cursor_visible=True
        self.name=self.__class__.__name__
        self.s_settings=app.config.get(
                self.name, {})
        self.setUI()
        self.app.installEventFilter(self)

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.MouseMove:
            if not self.cursor_visible:
                event.accept()
                return True
        return False

    def setUI(self):

        self.setContentsMargins(0,0,0,0)
        self.m_hlayout=QtWidgets.QVBoxLayout(self)#.m_hsplit)
        self.m_hlayout.setSpacing(0)
        self.m_hlayout.setContentsMargins(0,0,0,0)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def setViewClass(self, view_class): 

        self.view_class=view_class

    def clear(self):

        for index in range(self.m_hlayout.count(),-1, -1):
            item=self.m_hlayout.takeAt(index)
            if item: item.widget().hide()
        self.hide()

    def setView(self, view, how=None, focus=True):

        self.setCurrentView(view)
        if how=='reset':
            self.clear()
            self.m_hlayout.addWidget(view)
            self.show()
        elif how=='below':
            self.m_hlayout.addWidget(view)
            self.show()
        view.show()
        if focus: 
            view.setFocus()

    def addView(self, view):

        self.m_hlayout.addWidget(view)

    def focus(self, increment=1):

        if self.m_hlayout.count()<2:
            view=self.currentView()
            if view: view.setFocus()
        else:
            currentView=self.currentView()
            index=self.indexOf(currentView)
            index+=increment
            if index>=self.m_hlayout.count():
                index=0
            elif index<0:
                index=self.m_hlayout.count()-1
            view=self.widget(index)
            self.setCurrentView(view)

    def closeView(self, view=None, vid=None):

        if view is None:
            view=self.currentView()
        if vid is None and view:
            vid=view.id()
        index=None
        for f in range(self.m_hlayout.count()):
            item=self.m_hlayout.itemAt(f)
            if item and item.widget().id()==vid:
                view=item.widget()
                index=f
                break
        if not index is None:
            self.m_hlayout.removeWidget(view)
            view.close()
            index-=1
            if index<0: index=0
            if self.m_hlayout.count()>0:
                view=self.widget(index)
                self.setCurrentView(view)
                self.focusCurrentView()

    def open(self, model=None, how='reset', focus=True):

        if how=='reset':
            if self.view and self.view.model()==model: 
                return

        view=self.createView(model)
        if view: 
            self.setView(view, how, focus)
            self.viewCreated.emit(view)

    def createView(self, model):

        if self.view_class and model:
            self.count+=1
            view=self.view_class(self.app)
            view.setModel(model)
            self.views[self.count]=view
            return view

    def currentView(self): return self.view

    def setCurrentView(self, view):

        if view!=self.view: 
            self.view=view
            self.focusCurrentView()
            self.viewChanged.emit(self.view)

    def incrementUp(self, digit=1): 

        for d in range(digit): self.view.incrementUp()

    def incrementDown(self, digit=1): 

        for d in range(digit): self.view.incrementDown()

    def incrementLeft(self, digit=1): 

        for d in range(digit): self.view.incrementLeft()

    def incrementRight(self, digit=1): 

        for d in range(digit): self.view.incrementRight()

    def zoomIn(self, digit=1): 
        
        for d in range(digit): 
            self.view.changeScale(kind='zoomIn')

    def zoomOut(self, digit=1): 
        
        for d in range(digit): 
            self.view.changeScale(kind='zoomOut')

    def adjust(self): self.view.readjust()

    def keyPressEvent(self, event):

        if event.key()==QtCore.Qt.Key_Escape:
            if self.view: self.view.cleanUp()
        else:
            super().keyPressEvent(event)
    
    def toggleCursor(self): 

        if self.cursor_visible:
            cursor=QtGui.QCursor(QtCore.Qt.BlankCursor)
        else:
            cursor=QtGui.QCursor(QtCore.Qt.ArrowCursor)

        self.cursor_visible=not self.cursor_visible
        self.app.setOverrideCursor(cursor)

    def focusUpView(self): self.focus(-1)

    def focusDownView(self): self.focus(+1)

    def focusCurrentView(self): 

        self.deactivate(focusView=False)
        self.setFocus()
        view=self.app.window.main.display.view
        if view: view.setFocus()

    def deactivate(self, focusView=True):

        self.activated=False
        if focusView: self.focusCurrentView()

    def activate(self):

        self.activated=True
        self.show()
        self.setFocus()

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def cleanUp(self): 

        if self.view: self.view.cleanUp()

    def incrementFold(self): 
        
        if self.view: self.view.incrementFold()

    def decrementFold(self): 
        
        if self.view: self.view.decrementFold()
