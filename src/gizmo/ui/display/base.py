from PyQt5 import QtCore, QtWidgets

class BaseDisplay(QtWidgets.QWidget):

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
    selection=QtCore.pyqtSignal(
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

    def __init__(
            self, 
            *args, 
            app=None,
            window=None,
            objectName='Display',
            config={},
            **kwargs
            ):

        self.app=app
        self.m_config=config
        super().__init__(
                parent=window.main,
                objectName=objectName,
                )
        self.setup()
        window.resized.connect(self.update)
        self.selection.connect(app.selection)

    def setup(self):

        self.count=-1
        self.views={}
        self.view=None
        self.prev=None
        self.renders=[]
        self.setUI()
        self.setConfig()

    def setConfig(self):

        if self.app:
            c=self.app.config
            self.m_config=c.get(
                    'Display', {})

    def setUI(self):

        self.setContentsMargins(
                0,0,0,0)
        self.setContextMenuPolicy(
                QtCore.Qt.NoContextMenu)
        self.m_layout=QtWidgets.QVBoxLayout(
                self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(
                0,0,0,0)

    def clear(self):

        c=self.m_layout.count()
        for j in range(c,-1, -1):
            i=self.m_layout.takeAt(j)
            if i: i.widget().hide()
        self.hide()

    def setView(
            self, 
            view, 
            how=None, 
            focus=True
            ):

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

    def copyView(self, model):

        source=model.source()
        for r in self.app.renders:
            if r.isCompatible(source):
                return r.getView(model)

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

    def closeView(
            self, 
            view=None, 
            vid=None
            ):

        if not view:
            view=self.currentView()
        if not vid and view:
            vid=view.id()
        idx=None
        l=self.m_layout
        for f in range(l.count()):
            i=l.itemAt(f)
            if i and i.widget().id()==vid:
                idx=f
                view=i.widget()
                break
        if not idx is None:
            l.removeWidget(view)
            view.close()
            idx=max(idx-1, 0)
            if l.count()>0:
                view=self.widget(idx)
                self.setCurrentView(view)

    def open(
            self, 
            view=None,
            how='reset', 
            focus=True, 
            **kwargs
            ):

        if how=='reset' and self.view:
            nmodel=view.model()
            cmodel=self.view.model()
            if cmodel==nmodel: 
                return
        if view: 
            self.saveView(view)
            self.setView(
                    view, 
                    how, 
                    focus, 
                    **kwargs)
            self.viewCreated.emit(view)

    def saveView(self, view):

        self.count+=1
        self.views[self.count]=view

    def getRenderConfig(self, render):

        c=self.m_config
        g=c.get('View', {})
        v=render.view_class
        s=g.get(v.__name__, {})
        for k, v in g.items():
            if not k in s:
                s[k]=v
            sv=s[k]
            if type(sv)==dict:
                v.update(sv)
                s[k]=v
        return s

    def currentView(self): 
        return self.view

    def setCurrentView(self, view):

        if view!=self.view: 
            self.prev=self.view
            self.select(
                    self.prev, False)
            self.view=view
            self.select(
                    self.view, True)
            self.viewChanged.emit(
                    self.view, self.prev)

    def select(self, view, cond):

        if view:
            view.setProperty(
                    'selected', cond)
            view.style().unpolish(view)
            view.style().polish(view)

    def addView(self, view):
        self.m_layout.addWidget(view)

    def split(self, cond):
        pass

    def update(self): 
        pass
