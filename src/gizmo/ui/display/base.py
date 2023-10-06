from PyQt5 import QtCore, QtGui, QtWidgets

class BaseDisplay:

    annotationAdded=QtCore.pyqtSignal(
            object)
    annotationCreated=QtCore.pyqtSignal(
            object)
    annotationRegistered=QtCore.pyqtSignal(
            object)
    viewCreated=QtCore.pyqtSignal(
            object)
    viewChanged=QtCore.pyqtSignal(
            object, object)
    itemChanged = QtCore.pyqtSignal(
            object, object)
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

    def setup(self, app):

        self.app=app
        self.count=-1
        self.views={}
        self.view=None
        self.prev=None
        self.viewers=[]
        self.setUI()

    def addViewer(self, viewer):
        self.viewers+=[viewer]

    def setUI(self):

        self.setContentsMargins(0,0,0,0)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.m_layout=QtWidgets.QVBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0,0,0,0)

    def clear(self):

        count=self.m_layout.count()
        for index in range(count,-1, -1):
            item=self.m_layout.takeAt(index)
            if item: 
                item.widget().hide()
        self.hide()

    def setView(self, view, how=None, focus=True):

        self.setCurrentView(view)
        if how=='reset':
            self.clear()
            self.m_layout.addWidget(view)
        elif how=='below':
            self.m_layout.addWidget(view)
        self.show()
        view.show()
        if focus: 
            view.setFocus()

    def addView(self, view):

        self.m_layout.addWidget(view)

    def focus(self, increment=1):

        if self.m_layout.count()<2:
            view=self.currentView()
            if view: view.setFocus()
        else:
            currentView=self.currentView()
            index=self.indexOf(currentView)
            index+=increment
            if index>=self.m_layout.count():
                index=0
            elif index<0:
                index=self.m_layout.count()-1
            view=self.widget(index)
            self.setCurrentView(view)

    def closeView(self, view=None, vid=None):

        if not view:
            view=self.currentView()
        if not vid and view:
            vid=view.id()
        index=None
        for f in range(self.m_layout.count()):
            item=self.m_layout.itemAt(f)
            if item and item.widget().id()==vid:
                view=item.widget()
                index=f
                break
        if not index is None:
            self.m_layout.removeWidget(view)
            view.close()
            index-=1
            if index<0: index=0
            if self.m_layout.count()>0:
                view=self.widget(index)
                self.setCurrentView(view)
                self.focusCurrentView()

    def open(self, 
             model=None, 
             how='reset', 
             focus=True,
             **kwargs):

        if how=='reset':
            if self.view and self.view.model()==model: 
                return

        view=self.createView(model)
        if view: 
            self.setView(
                    view, how, focus, **kwargs)
            self.viewCreated.emit(view)

    def createView(self, model):

        for v in self.viewers:
            view=v.getView(model)
            if view: 
                self.count+=1
                self.views[self.count]=view
                return view

    def currentView(self): 
        return self.view

    def setCurrentView(self, view):

        if view!=self.view: 
            self.prev=self.view
            self.view=view
            self.focusCurrentView()
            self.viewChanged.emit(
                    self.view, self.prev)

    def incrementUp(self, digit=1): 

        for d in range(digit): 
            self.view.incrementUp()

    def incrementDown(self, digit=1): 

        for d in range(digit): 
            self.view.incrementDown()

    def incrementLeft(self, digit=1): 

        for d in range(digit): 
            self.view.incrementLeft()

    def incrementRight(self, digit=1): 

        for d in range(digit): 
            self.view.incrementRight()

    def zoomIn(self, digit=1): 
        
        for d in range(digit): 
            self.view.changeScale(kind='zoomIn')

    def zoomOut(self, digit=1): 
        
        for d in range(digit): 
            self.view.changeScale(kind='zoomOut')

    def adjust(self): 
        self.view.readjust()

    def keyPressEvent(self, event):

        if event.key()==QtCore.Qt.Key_Escape:
            if self.view: 
                self.view.cleanUp()
        else:
            super().keyPressEvent(event)
    
    def focusUp(self): 
        self.focus(-1)

    def focusDown(self): 
        self.focus(+1)

    def focusCurrentView(self): 

        self.deactivate(focusView=False)
        if self.view: 
            self.view.setFocus()

    def deactivate(self, focusView=True):

        self.activated=False
        if focusView: 
            self.focusCurrentView()

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

        if self.view: 
            self.view.cleanUp()

    def incrementFold(self): 
        
        if self.view: 
            self.view.incrementFold()

    def decrementFold(self): 
        
        if self.view: 
            self.view.decrementFold()
