from PyQt5 import QtCore

class ItemMixin:

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

    def setModel(self, model):

        if self.m_scene:
            self.clearScene()
        if model:
            self.m_model = model
            self.setItems()
            self.addItems()
            self.updateView()
            self.setVisibleItem()

    def updateSceneRect(self):

        self.updateItemScale()
        h = self.m_layout.m_mode.pageSpacing
        l, r, h = self.m_layout.load(
                items=self.m_items.values(),
                height=h)
        self.scene().setSceneRect(
                l, 0.0, r-l, h)

    def updateItemScale(self):

        s=self.size()
        l=self.m_layout
        w=l.width(s.width())
        h=l.height(s.height())

        items=self.m_items.values()
        for i in items:
            x=self.logicalDpiX()
            y=self.logicalDpiY()
            i.setResol(x, y)
            dw= i.displayedWidth()
            dh = i.displayedHeight()
            fitPageSize=[w/float(dw), h/float(dh)]
            width_ratio=w/dw
            scale = {
                'ScaleFactor': i.scale,
                'FitToWindowWidth': width_ratio,
                'FitToWindowHeight': min(fitPageSize)
                }
            s=scale[self.scaleMode]
            i.setScaleFactor(s)

    def setItems(self):

        if self.item_class:
            self.m_items = {}
            c=self.m_config.get('Item', {})
            s=self.m_model.elements()
            sf=self.scaleFactor
            v=s.values()
            for j, e in enumerate(v):
                i = self.item_class(
                        config=c,
                        index=j+1,
                        element=e, 
                        scaleFactor=sf,
                        )
                self.m_items[j+1]=i

    def addItems(self):

        if self.m_scene:
            for i in self.m_items.values():
                self.m_scene.addItem(i)

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
