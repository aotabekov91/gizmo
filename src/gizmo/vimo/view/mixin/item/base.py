from PyQt5 import QtCore
from gizmo.vimo.item import Item

from ...base import View
from ..scene import Scene
from ..layout import Layout

class Items(
        Scene, 
        Layout, 
        View
        ):

    hasItems=True
    item_class=Item
    indexChanged=QtCore.pyqtSignal(
            object, object)

    def getItems(self):
        return self.m_items.items()

    def count(self):
        return len(self.m_items) 

    def item(self, idx):
        return self.m_items.get(idx, None)

    def setup(self):

        self.m_curr=1
        self.m_prev=None
        self.m_items={}
        self.indexChanged.connect(
                self.app.window.viewIndexChanged)
        super().setup()

    def setModel(self, model):

        self.clearScene()
        if model:
            super().setModel(model)
            self.setItems()
            self.redraw()

    def setItems(self):

        self.m_items={}
        c=self.m_config.get('Item', {})
        if self.item_class:
            elems=self.m_model.elements()
            for j, e in enumerate(elems.values()): 
                i=self.item_class(
                        config=c,
                        index=j+1,
                        element=e,
                        )
                self.setupItem(i)

    def setupItem(self, i):

        idx=i.index()
        i.setVisible(False)
        self.m_items[idx]=i
        x=self.logicalDpiX()
        y=self.logicalDpiY()
        i.setResol(x, y)
        self.m_scene.addItem(i)

    def redraw(self):

        self.redrawScene()
        self.redrawView()
        self.setVisibleItem()

    def redrawScene(self):

        h = self.m_layout.m_mode.pageSpacing
        l, r, h = self.m_layout.load(
                items=self.m_items.values(),
                height=h)
        self.m_scene.setSceneRect(
                l, 0.0, r-l, h)

    def redrawView(self):

        vv, hv = 0, 0
        s = self.m_scene
        r = s.sceneRect()
        l, t = r.left(), r.top()
        w, h = r.width(), r.height()
        for j, i in self.m_items.items():
            i.setVisible(True)
            pbr = i.boundingRect()
            pos = pbr.translated(i.pos())
            h += pos.height()
        self.setSceneRect(l, t, w, h)
        self.verticalScrollBar().setValue(vv)
        self.horizontalScrollBar().setValue(hv)
        self.viewport().update()

    def setCurrentItem(self, item):

        idx=item.index()
        self.setCurrentIndex(idx)

    def setCurrentIndex(self, idx):

        if self.m_curr!=idx:
            self.m_prev=self.m_curr
            self.m_curr=idx
            self.indexChanged.emit(
                    self, idx)

    def refresh(self):

        for j, i in self.getItems():
            i.refresh(dropCache=True)

    def currentItem(self):
        return self.item(self.m_curr)

    def currentIndex(self):
        return self.m_curr

    def updateCurrent(self, refresh=False):

        i=self.currentItem()
        i.refresh(dropCache=refresh)

    def updateVisibile(self, refresh=False):

        for i in self.m_items.values(): 
            if i.isVisible():
                i.refresh(refresh)

    def setVisibleItem(self):

        r=self.viewport().rect()
        x, w = int(r.width()/2-5), 10
        y, h =int(r.height()/2-5), 10
        v=QtCore.QRect(x, y, w, h)
        i=self.items(v)
        if i:
            self.setCurrentItem(i[0])

    def visibleItems(self): 

        r=self.viewport().rect()
        return self.items(r)
