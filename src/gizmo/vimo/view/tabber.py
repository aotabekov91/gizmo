from gizmo.utils import tag
from PyQt5 import QtWidgets, QtCore

from .base import View

class Tabber(
        View,
        QtWidgets.QStackedWidget,
        ):

    hasTabs=True
    tab_class=None

    def setup(self):

        self.setConf()
        self.setName()
        self.m_current_tab=None
        self.m_label=QtWidgets.QLabel(self.name)

    def newTab(self):

        ctab=self.m_current_tab
        if ctab:
            ntab=self.createTab()
            ntab.setModel(ctab.model())
            ridx=ctab.rootIndex()
            ntab.setRootIndex(ridx)
            self.setFocus()

    def createTab(self):

        ntab=self.getTab()
        self.addTab(ntab)
        self.setTab(ntab)
        return ntab

    def goTo(self, digit=1):

        ntab=self.widget(digit-1)
        if ntab:
            self.setTab(ntab)
            self.setFocus()

    def tabGoToNext(self):

        ctab=self.m_current_tab
        idx=ctab.m_tab_idx+1
        if idx>self.count()-1: idx=0
        ntab=self.widget(idx)
        print(ntab)
        if ntab:
            self.setTab(ntab)
            self.setFocus()

    def setModel(self, model):

        if not self.m_current_tab:
            tab=self.getTab()
            self.addTab(tab)
            self.setTab(tab)
        self.m_current_tab.setModel(model)

    def getTab(self):

        return self.tab_class(
                parent=self,
                app=self.app,
                index=self.m_id,
                name=self.m_name,
                config=self.m_config,
                objectName=self.objectName())

    def addTab(self, tab):

        tab.m_tabber=self
        tab.hasTabber=True
        tab.m_tab_idx=self.addWidget(tab)
        tab.m_tab_label=QtWidgets.QLabel()
        tab.m_tab_name=tab.m_tab_idx

    @tag('<c-d><c-d>', modes=['normal|View'])
    def delTab(self, tab=None):

        tab = tab or self.m_current_tab
        print(tab)
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
            self.setTab(tab)
            self.setFocus()

    def setTab(self, tab):

        self.m_current_tab=tab
        self.setCurrentIndex(tab.m_tab_idx)

    def setFocus(self):

        super().setFocus()
        if self.m_current_tab:
            self.m_current_tab.setFocus()
            self.focusGained.emit(
                    self.m_current_tab)
