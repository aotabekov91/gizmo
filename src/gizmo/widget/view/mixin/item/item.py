from PyQt5 import QtCore

from .creator import Creator
from ...item import BaseItem

class ItemMixin:

    item_class=BaseItem

    itemChanged = QtCore.pyqtSignal(
            object, object)
    itemPainted = QtCore.pyqtSignal(
            object, object, object, object, object)
    itemHoverMoveOccured = QtCore.pyqtSignal(
            [object, object, object])
    itemMouseMoveOccured = QtCore.pyqtSignal(
            [object, object, object])
    itemMousePressOccured = QtCore.pyqtSignal(
            [object, object, object])
    itemMouseReleaseOccured = QtCore.pyqtSignal(
            [object, object, object])
    itemMouseDoubleClickOccured = QtCore.pyqtSignal(
            [object, object, object])

    elementCreated=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
        self.pool=QtCore.QThreadPool()

    def setupConnect(self):

        super().setupConnect()
        if not self.position:
            return
        p=getattr(
                self.app, 
                self.position, 
                None)
        if p:
            self.itemMouseDoubleClickOccured.connect(
                    p.itemMouseDoubleClickOccured)
            self.itemMouseReleaseOccured.connect(
                    p.itemMouseReleaseOccured)
            self.itemMouseMoveOccured.connect(
                    p.itemMouseMoveOccured)
            self.itemMousePressOccured.connect(
                    p.itemMousePressOccured)
            self.itemHoverMoveOccured.connect(
                    p.itemHoverMoveOccured)
            self.itemChanged.connect(
                p.itemChanged)
            self.itemPainted.connect(
                    p.itemPainted)

    def on_itemAdded(self, item):

        for f in [
                  'painted',
                  'mouseMoveOccured',
                  'hoverMoveOccured',
                  'mousePressOccured',
                  'mouseReleaseOccured',
                  'mouseDoubleClickOccured',
                 ]:
            s=getattr(item, f, None)
            if s:
                i=f[0].upper()+f[1:]
                n=f'on_item{i}'
                o=getattr(self, n)
                s.connect(o)

    def on_itemPainted(self, p, o, w, i):
        self.itemPainted.emit( p, o, w, i, self)

    def on_itemMouseDoubleClickOccured(self, i, e):
        self.itemMouseDoubleClickOccured.emit(
                self, i, e)

    def on_itemMousePressOccured(self, i, e):
        self.itemMousePressOccured.emit(self, i, e)

    def on_itemMouseReleaseOccured(self, i, e):
        self.itemMouseReleaseOccured.emit(self, i, e)

    def on_itemMouseMoveOccured(self, i, e):
        self.itemMouseMoveOccured.emit(self, i, e)

    def on_itemHoverMoveOccured(self, i, e):
        self.itemHoverMoveOccured.emit(self, i, e)

    def setItems(self):

        m=self.m_model
        self.m_items={}
        sf=self.scaleFactor
        c=self.m_config.get('Item', {})
        c=Creator(
                model=m,
                config=c,
                view=self,
                scaleFactor=sf,
                klass=self.item_class,
                )
        c.signals.created.connect(
                self.on_itemCreated)
        c.signals.finished.connect(
                self.on_itemsCreated)
        self.pool.start(c)

    def on_itemCreated(self, item):
        self.setupItem(item)

    def on_itemsCreated(self):

        self.updateView()
        self.setVisibleItem()

    def setupItem(self, i):

        idx=i.index()
        i.setVisible(False)
        self.m_items[idx]=i
        x=self.logicalDpiX()
        y=self.logicalDpiY()
        i.setResol(x, y)

    def setModel(self, model):

        if self.m_scene:
            self.clearScene()
        if model:
            self.m_model = model
            self.setItems()

    def updateSceneRect(self):

        self.updateScales()
        h = self.m_layout.m_mode.pageSpacing
        l, r, h = self.m_layout.load(
                items=self.m_items.values(),
                height=h)
        self.scene().setSceneRect(
                l, 0.0, r-l, h)

    def updateScales(self):

        i=self.item(1)
        if i:
            s=self.calculateScale(i)
        if i and s:
            v=self.getItems().values()
            for i in v:
                i.setScaleFactor(s)

    def calculateScale(self, i):

        s=self.size()
        l=self.m_layout
        w=l.width(s.width())
        h=l.height(s.height())
        x=self.logicalDpiX()
        y=self.logicalDpiY()
        i.setResol(x, y)

        ds = i.displayedSize()
        dw, dh = ds 
        if not dw: 
            return
        fitPageSize=[w/float(dw), h/float(dh)]
        width_ratio=w/dw
        scale = {
            'ScaleFactor': i.scale,
            'FitToWindowWidth': width_ratio,
            'FitToWindowHeight': min(fitPageSize)
            }
        return scale[self.scaleMode]

    def setCurrentItem(self, item):

        idx=item.index()
        self.setCurrentIndex(idx)
        self.itemChanged.emit(self, item)

    def setScaleFactor(self, factor):

        if self.scaleFactor != factor:
            if self.scaleMode == 'ScaleFactor':
                self.scaleFactor = factor
                for i in self.m_items.values():
                    i.setScaleFactor(factor)
                self.updateView()

    def refresh(self):

        for i in self.getItems():
            i.refresh(dropCache=True)

    def update(self, refresh=False):

        i=self.currentItem()
        i.refresh(dropCache=refresh)

    def updateAll(self, refresh=False):

        for i in self.m_items.values(): 
            if i.isVisible():
                i.refresh(refresh)

    def setVisibleItem(self):

        r=self.viewport().rect()
        x, w = int(r.width()/2-5), 10
        y, h =int(r.height()/2-5), 10
        v=QtCore.QRect(x, y, w, h)
        if hasattr(self, 'items'):
            items=self.items(v)
            if items:
                item=items[0]
                self.setCurrentItem(item)

    def setZoomFactor(self, zf):

        pos = self.getPosition()
        for i in self.m_items.values(): 
            n_zf=zf*i.scale
            i.setScaleFactor(n_zf)
        self.updateView(*pos)
