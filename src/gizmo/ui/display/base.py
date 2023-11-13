from PyQt5 import QtCore, QtWidgets

class BaseDisplay(QtWidgets.QWidget):

    viewSet=QtCore.pyqtSignal(object)
    viewChanged=QtCore.pyqtSignal(object)
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
        window.resized.connect(self.update)
        self.setup()

    def setup(self):

        self.count=-1
        self.views={}
        self.m_curr=None
        self.m_prev=None
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
            ):

        self.setCurrentView(view)
        if how=='reset':
            self.clear()
            self.m_layout.addWidget(view)
        elif how=='below':
            self.m_layout.addWidget(view)
        self.show()
        view.show()

    def copyView(self, v):

        if v and v.check('canCopy'): 
            return v.copy()

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

    def setupView(
            self, 
            view=None,
            how='reset', 
            **kwargs
            ):

        if how=='reset' and self.m_curr:
            nmodel=view.model()
            cmodel=self.m_curr.model()
            if cmodel==nmodel: 
                return
        if view: 
            self.count+=1
            self.views[self.count]=view
            self.setView(
                    view, how, **kwargs)
            self.viewSet.emit(view)

    def currentView(self): 
        return self.m_curr

    def setCurrentView(self, view):

        if view!=self.m_curr: 
            self.m_curr, self.m_prev=view, self.m_curr
            self.viewChanged.emit(self.m_curr)

    def addView(self, view):
        self.m_layout.addWidget(view)
