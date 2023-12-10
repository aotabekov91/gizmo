from PyQt5 import QtCore
from gizmo.vimo.item import Item

from .scene import Scene
from .layout import Layout

class Items(Scene, Layout):

    hasItems=True
    item_class=Item
    indexChanged=QtCore.pyqtSignal(object)

    def getItems(self):
        return self.m_items.items()

    def count(self):
        return len(self.m_items) 

    def item(self, idx=None, element=None):

        if element:
            for i in self.m_items.values():
                if i.element()!=element:
                    continue
                return i
        else:
            return self.m_items.get(idx, None)


    def setup(self):

        self.m_curr=1
        self.m_items={}
        self.m_prev=None
        self.m_fetched=0
        self.connectSlider()
        super().setup()

    def connectSlider(self):

        hbar=self.verticalScrollBar()
        hbar.valueChanged.connect(self.test)

    def canFetch(self):
        return self.m_fetched<self.count()

    def test(self, value):

        # if not self.canFetch(): 
        #     return
        # ii=self.m_items[1]
        # v=ii.boundingRect().height()
        # v=value/float(v*self.count())
        # v=int(v)+1
        # print(v)
        # for i in range(v-1, v+2):
        #     item=self.m_items.get(i)
        #     if not item: continue
        #     if not item.scene():
        #         self.m_fetched+=1
        #         self.m_scene.addItem(item)

        # print(v)

        v=0
        for i in self.m_items.values():
            pbr = i.boundingRect()
            pos = pbr.translated(i.pos())
            if value<=v or v==0:
                if not i.scene():
                    self.m_fetched+=1
                    self.m_scene.addItem(i)
            else:
                v+=pos.height()

        # if not i.scene():
        #     self.m_scene.addItem(i)

    def setModel(self, model):

        self.clearScene()
        if model and id(self.m_model)!=id(model):
            self.modelIsToBeChanged.emit(
                    self, self.m_model)
            self.m_model=model
            self.kind=model.kind
            self.setItems(model)
            self.redraw()

    def setItems(self, model):

        self.m_items={}
        c=self.m_config.get('Item', {})
        if self.item_class:
            elems=model.elements()
            for j, e in enumerate(elems.values()): 
                i=self.item_class(
                        config=c,
                        index=j+1,
                        element=e,
                        )
                self.setupItem(i)
                if j>2: break
        self.modelChanged.emit(model)
        self.modelLoaded.emit(self, model)

    def setupItem(self, i):

        idx=i.index()
        i.setVisible(False)
        self.m_items[idx]=i
        x=self.logicalDpiX()
        y=self.logicalDpiY()
        i.setResol(x, y)
        # self.m_scene.addItem(i)

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

    def redrawView(self, *args, **kwargs):

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

    def setCurrentIndex(self, idx):

        if self.m_curr!=idx:
            c, p = idx, self.m_curr
            self.m_curr, self.m_prev=c, p
        self.indexChanged.emit(self.m_curr)

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
        idx=self.m_curr
        if i: idx=i[0].index()
        self.setCurrentIndex(idx)

    def visibleItems(self): 

        r=self.viewport().rect()
        return self.items(r)
