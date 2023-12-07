from PyQt5 import QtWidgets, QtCore

from . import mixin, base

class Tabber(
        base.View,
        QtWidgets.QStackedWidget,
        ):

    hasTabs=True
    tab_class=None
    current_tab=None
    tabViewCreated=QtCore.pyqtSignal(
            object)

    def setup(self):

        super().setup()
        self.tabViewCreated.connect(
                self.tabRegister)

    def tabRegister(self, view):
        self.app.uiman.setupUI(ui=view)

    def tabCopy(self, tab=None):

        ptab=tab or self.current_tab
        if ptab and hasattr(ptab, 'canCopy'): 
            copy=ptab.copy()
            self.tabViewCreated.emit(copy)
            return copy

    def tabAddNew(self, copy=False):

        c=self.current_tab
        if copy and self.check('canCopy', c):
            n=c.copy()
        else:
            n=self.tabGet()
        h=getattr(self.app, 'handler', None)
        if h: h.connectView(n)
        self.tabAdd(n)
        self.tabSet(n)
        self.setFocus()
        return n

    def tabMove(self, kind=None, digit=None):

        idx=self.currentIndex()
        w=self.widget(idx)
        if kind=='left':
            idx=max(0, idx-1)
        elif kind=='right':
            idx+=1
        elif type(digit)==int:
            idx=digit-1
        else:
            return
        self.removeWidget(w)
        self.insertWidget(idx, w)
        self.tabSet(w)
        self.setFocus()

    def tabGoTo(self, kind=None, digit=None):

        if kind=='prev':
            c=self.currentIndex()
            digit=max(0, c-1)
        elif kind=='next':
            c=self.currentIndex()
            digit=min(self.count()-1, c+1)
        elif type(digit)==int:
            digit-=1
        elif digit is None:
            digit=self.count()
        else:
            return
        ntab=self.widget(digit)
        if ntab: self.tabSet(ntab)
        self.setFocus()

    def tabGoToNext(self):

        ctab=self.current_tab
        idx=ctab.m_tab_idx+1
        if idx>self.count()-1: idx=0
        ntab=self.widget(idx)
        if ntab:
            self.tabSet(ntab)
            self.setFocus()

    def tabGet(self):

        view=self.tab_class(
                parent=self,
                app=self.app,
                index=self.m_id,
                name=self.m_name,
                config=self.m_config,
                objectName=self.objectName())
        self.tabViewCreated.emit(view)
        return view

    def tabAdd(self, tab):

        tab.m_tabber=self
        tab.hasTabber=True
        tab.m_tab_idx=self.addWidget(tab)
        tab.m_tab_label=QtWidgets.QLabel()
        tab.m_tab_name=tab.m_tab_idx

    def insertWidget(self, idx, w):

        super().insertWidget(idx, w)
        self.tabReindex()

    def removeWidget(self, w):

        super().removeWidget(w)
        self.tabReindex()
        return w

    def tabReindex(self):

        for i in range(self.count()):
            w=self.widget(i)
            w.m_tab_idx=i

    def tabClose(self, tab=None, limit=1):

        if self.count()<=limit: return
        tab = tab or self.current_tab
        if tab:
            idx=tab.m_tab_idx
            tab.m_tabber=None
            tab.hasTabber=False
            self.removeWidget(tab)
            delattr(tab, 'm_tabber')
            delattr(tab, 'm_tab_idx')
            delattr(tab, 'hasTabber')
        tab=self.widget(idx-1)
        if tab: self.tabSet(tab)
        self.setFocus()

    def tabSet(self, tab):

        self.current_tab=tab
        self.setCurrentIndex(tab.m_tab_idx)

    def setFocus(self):

        super().setFocus()
        if self.current_tab:
            self.current_tab.setFocus()
            self.focusGained.emit(
                    self.current_tab)

    def setModel(self, model, **kwargs):

        if model:
            if not self.current_tab:
                self.tabAddNew()
            self.m_model=model
            self.current_tab.setModel(model)
