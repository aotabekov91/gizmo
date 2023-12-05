from PyQt5 import QtWidgets, QtCore

from .base import View

class Tabber(
        View,
        QtWidgets.QStackedWidget,
        ):

    hasTabs=True
    tab_class=None
    current_tab=None

    def tabAddNew(self, copy=False):

        ptab=self.current_tab
        if copy and ptab:
            if hasattr(ptab, 'canCopy'):
                ntab=ptab.copy()
        else:
            ntab=self.tabGet()
        self.tabAdd(ntab)
        self.tabSet(ntab)
        self.setFocus()
        return ntab

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
        if ntab:
            self.tabSet(ntab)
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

        return self.tab_class(
                parent=self,
                app=self.app,
                index=self.m_id,
                name=self.m_name,
                config=self.m_config,
                objectName=self.objectName())

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

    def tabReindex(self):

        for i in range(self.count()):
            w=self.widget(i)
            w.m_tab_idx=i

    def tabClose(self, tab=None):

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
        if tab:
            self.tabSet(tab)
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
