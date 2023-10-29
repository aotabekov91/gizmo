from PyQt5 import QtWidgets, QtCore, QtGui

from .item import Item
from ..scene import Scene
from .layout import Layout
from .cursor import Cursor

class View(QtWidgets.QGraphicsView):

    position='display'
    scaleModeChanged = QtCore.pyqtSignal(
            object, object)
    scaleFactorChanged = QtCore.pyqtSignal(
            object, object)
    continuousModeChanged = QtCore.pyqtSignal(
            bool, object)
    focusGained=QtCore.pyqtSignal(
            object)
    resized=QtCore.pyqtSignal(
            object, object)
    modelModified = QtCore.pyqtSignal(
            object)
    layoutModeChanged = QtCore.pyqtSignal(
            object)
    selection=QtCore.pyqtSignal(
            object, object)
    itemChanged = QtCore.pyqtSignal(
            object, object)
    itemPainted = QtCore.pyqtSignal(
            object, object, object, object, object)
    positionChanged = QtCore.pyqtSignal(
            object, object, object, object)
    keyPressOccurred=QtCore.pyqtSignal(
            [object, object])
    hoverMoveOccured = QtCore.pyqtSignal(
            [object, object])
    mouseMoveOccured = QtCore.pyqtSignal(
            [object, object])
    mousePressOccured = QtCore.pyqtSignal(
            [object, object])
    mouseReleaseOccured = QtCore.pyqtSignal(
            [object, object])
    mouseDoubleClickOccured = QtCore.pyqtSignal(
            [object, object])
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

    def __init__(
            self, 
            app, 
            config={},
            item_class=Item,
            scene_class=Scene,
            layout_class=Layout,
            cursor_class=Cursor,
            objectName='View',
            foldlevel=0,
            scaleFactor=1.,
            zoomFactor = 0.1,
            continuousView=True,
            scaleMode='FitToWindowHeight',
            **kwargs,
            ):

        self.zoom=1
        self.app=app
        self.m_cut=[]
        self.m_cache={}
        self.m_items=[]
        self.m_yanked=[]
        self.m_selected=[]
        self.m_elements={}
        self.m_id=id(self)
        self.m_curr = None 
        self.m_prev = None 
        self.m_model = None
        self.m_config=config
        self.foldlevel=foldlevel
        self.scaleMode=scaleMode
        self.scaleFactor=scaleFactor
        self.zoomFactor = zoomFactor  
        self.continuousView=continuousView
        self.item_class=item_class
        self.scene_class=scene_class
        self.cursor_class=cursor_class
        self.layout_class=layout_class
        self.m_cursor=QtCore.Qt.ArrowCursor
        super().__init__(
                objectName=objectName,
                **kwargs,
                )
        self.setSettings()
        self.setup(
                scene_class, 
                layout_class, 
                cursor_class,
                )
        self.connect()

    def setSettings(self):

        c=self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setup(
            self, 
            scene_class, 
            layout_class,
            cursor_class,
              ):

        self.setupLayout()
        self.setupScene()
        self.setupCursor()
        self.setupView()

    def setupView(self):

        self.setDragMode(
                QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.setProperty('selected', False)
        self.setContentsMargins(0,0,0,0)
        self.setAcceptDrops(False)

    def setupCursor(self):

        config=self.m_config.get(
                'Cursor', {})
        self.cursor=self.cursor_class(
                self, config=config)

    def setupLayout(self):

        config=self.m_config.get(
                'Layout', {})
        self.m_layout = self.layout_class(
                self, config=config)

    def setItem(self, e):

        config=self.m_config.get(
                'Item', {})
        i = self.item_class(
                element=e, 
                view=self,
                index=e.index(),
                scaleFactor=self.scaleFactor,
                config=config,
                )
        e.setItem(i)
        self.m_items += [i]
        self.scene().addItem(i)

    def setupScene(self):

        self.m_scene=self.scene_class()
        self.m_scene.itemAdded.connect(
                self.on_itemAdded)
        self.setScene(self.m_scene)
        self.scene().setBackgroundBrush(
                QtGui.QColor('black'))

    def setId(self, vid):
        self.m_id=vid

    def id(self):
        return self.m_id

    def setLayout(self, layout):

        self.m_layout=layout
        self.layoutModeChanged.emit(self)

    def selected(self):
        return self.m_selected

    def deselect(self, item=None):
        self.m_selected=[]

    def select(self, selections=[]): 

        if self.m_selected: 
            self.deselect(self.m_selected)
        self.m_selected=selections
        self.selection.emit(
                self, self.m_selected)

    def show(self):

        super().show()
        self.readjust()
        self.setFocus()

    def connect(self):

        d=self.app.display
        self.mouseDoubleClickOccured.connect(
                d.viewMouseDoubleClickOccured)
        self.mouseReleaseOccured.connect(
                d.viewMouseReleaseOccured)
        self.mouseMoveOccured.connect(
                d.viewMouseMoveOccured)
        self.mousePressOccured.connect(
                d.viewMousePressOccured)
        self.hoverMoveOccured.connect(
                d.viewHoverMoveOccured)
        self.itemMouseDoubleClickOccured.connect(
                d.itemMouseDoubleClickOccured)
        self.itemMouseReleaseOccured.connect(
                d.itemMouseReleaseOccured)
        self.itemMouseMoveOccured.connect(
                d.itemMouseMoveOccured)
        self.itemMousePressOccured.connect(
                d.itemMousePressOccured)
        self.itemHoverMoveOccured.connect(
                d.itemHoverMoveOccured)
        self.itemChanged.connect(
            d.itemChanged)
        self.positionChanged.connect(d.positionChanged)
        self.itemPainted.connect(d.itemPainted)
        self.resized.connect(self.readjust)
        self.selection.connect(
                self.app.display.selection)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.resized.emit(self, event)

    def mouseMoveEvent(self, event):
        
        super().mouseMoveEvent(event)
        self.mouseMoveOccured.emit(self, event)

    def mousePressEvent(self, event):

        super().mousePressEvent(event)
        self.mousePressOccured.emit(self, event)

    def mouseReleaseEvent(self, event):
        
        super().mouseReleaseEvent(event)
        self.mouseReleaseOccured.emit(self, event)

    def mouseDoubleClickEvent(self, event):

        super().mouseDoubleClickEvent(event)
        self.mouseDoubleClickOccured.emit(self, event)

    def on_itemAdded(self, item):

        item.itemPainted.connect(
                self.on_itemPainted)
        item.mouseDoubleClickOccured.connect(
                self.on_itemMouseDoubleClickOccured)
        item.mousePressOccured.connect(
                self.on_itemMousePressOccured)
        item.mouseReleaseOccured.connect(
                self.on_itemMouseReleaseOccured)
        item.mouseMoveOccured.connect(
                self.on_itemMouseMoveOccured)
        item.hoverMoveOccured.connect(
                self.on_itemHoverMoveOccured)

    def on_itemPainted(
            self, 
            painter, 
            options, 
            widget, 
            page):

        self.itemPainted.emit(
                painter, 
                options, 
                widget, 
                page, 
                self)

    def on_itemMouseDoubleClickOccured(
            self, item, event):

        self.itemMouseDoubleClickOccured.emit(
                self, item, event)

    def on_itemMousePressOccured(
            self, item, event):

        self.itemMousePressOccured.emit(
                self, item, event)

    def on_itemMouseReleaseOccured(
            self, item, event):

        self.itemMouseReleaseOccured.emit(
                self, item, event)

    def on_itemMouseMoveOccured(
            self, item, event):

        self.itemMouseMoveOccured.emit(
                self, item, event)

    def on_itemHoverMoveOccured(
            self, item, event):

        self.itemHoverMoveOccured.emit(
                self, item, event)

    def setFoldLevel(self, level): 
        self.foldlevel=max(level, 0)

    def foldLevel(self): 
        return self.foldlevel

    def incrementFold(self): 
        self.setFoldLevel(self.foldLevel()+1)

    def decrementFold(self): 
        self.setFoldLevel(self.foldLevel()-1)

    def visibleItems(self): 

        rect=self.viewport().rect()
        return self.items(rect)

    def model(self): 
        return self.m_model

    def modelId(self):

        if self.m_model:
            return self.m_model.id()

    def element(self, idx):

        if self.m_model:
            return self.m_model.element(idx)

    def elements(self):

        if self.m_model:
            return self.m_model.elements()

    def increment(self, kind): 
        pass

    def derement(self, kind):
        pass

    def prev(self): 
        pass

    def next(self): 
        pass

    def open(self, *arg, **kwargs):
        pass

    def gotoEnd(self): 
        pass

    def gotoBegin(self): 
        pass

    def save(self): 
        pass

    def cleanUp(self): 
        pass

    def paint(self): 
        pass

    def count(self): 
        return len(self.m_items)

    def getItems(self): 
        return self.m_items

    def prepareView(self, *args, **kwargs):
        pass

    def prepareScene(self, *args, **kwarags):
        pass

    def initialize(self):
        self.setVisiblePage()

    def fitToWindowWidth(self):
        self.setScaleMode('FitToWindowWidth')

    def fitToWindowHeight(self):
        self.setScaleMode('FitToWindowHeight')

    def gotoFirst(self): 
        self.goto(1)

    def item(self, idx=None):

        if idx is not None:
            idx-=1
        else:
            idx=self.m_curr
        return self.m_items[idx]

    def itemId(self, item=None):

        if not item:
            item=self.currentItem()
        return item.index()

    def currentItem(self):
        return self.item()

    def readjust(self):

        l, t=self.getPosition()
        self.updateView(l, t)

    def name(self):

        if self.m_model:
            return self.m_model.id()
        return super().name()
    
    def setModel(self, model):

        self.scene().clear()
        self.m_model=model
        if model:
            self.m_model = model
            self.setItems(model)
            self.updateView()
            self.initialize()

    def updateView(self, x=None, y=None):

        l, t = self.getPosition()
        top = y or t
        left = x or l 
        s=self.size()
        l=self.m_layout
        vw=l.width(s.width())
        vh=l.height(s.height())
        self.prepareScene(vw, vh)
        self.prepareView(left, top)

    def setItems(self, model):

        self.m_items = []
        elem=model.elements()
        for e in elem.values():
            self.setItem(e)

    def getPosition(self):

        if self.m_curr:
            i=self.m_items[self.m_curr]
            r=i.boundingRect().translated(i.pos())
            tl=self.viewport().rect().topLeft()
            tl=self.mapToScene(tl)
            x=(tl.x() -r.x())/r.width()
            y=(tl.y() -r.y())/r.height()
            return x, y
        return 0, 0

    def reportPosition(self):

        x, y = self.getPosition()
        i=self.currentItem()
        self.positionChanged.emit(
                self, i, x, y) 

    def setVisiblePage(self):

        r=self.viewport().rect()
        x, w = int(r.width()/2-5), 10
        y, h =int(r.height()/2-5), 10
        v=QtCore.QRect(x, y, w, h)
        items=self.items(v)
        if items:
            e=items[0].element()
            m_curr=e.index()-1
            self.setCurrent(m_curr)

    def setScaleFactor(self, factor):

        if self.scaleFactor != factor:
            if self.scaleMode() == 'ScaleFactor':
                self.scaleFactor = factor
                for i in self.m_items:
                    i.setScaleFactor(factor)
                self.updateView()

    def setScaleMode(self, mode):

        self.scaleMode = mode
        self.adjustScrollBarPolicy()
        self.updateView()
        self.scaleModeChanged.emit(mode, self)

    def scaleMode(self):
        return self.scaleMode

    def adjustScrollBarPolicy(self):

        sm = self.scaleMode
        if sm == 'ScaleFactor':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif sm == 'FitToWindowWidth':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
        elif sm == 'FitToWindowHeight':
            self.setHorizontalScrollBarPolicy(
                    QtCore.Qt.ScrollBarAlwaysOff)
            policy = QtCore.Qt.ScrollBarAlwaysOff
            if self.continuousView:
                policy = QtCore.Qt.ScrollBarAsNeeded

    def setCurrent(self, pnum):

        if self.m_curr!=pnum:
            self.m_prev=self.m_curr
            self.m_curr=pnum
            c=self.currentItem()
            self.itemChanged.emit(self, c)
        self.reportPosition()
        
    def refresh(self):

        for i in self.getItems():
            i.refresh(dropCache=True)

    def update(self, refresh=False):

        i=self.currentItem()
        i.refresh(dropCache=refresh)

    def updateAll(self, refresh=False):

        for i in self.m_items: 
            if i.isVisible():
                i.refresh(refresh)

    def prev(self):

        c=self.count()
        l=self.m_layout
        cur=l.previousPage(self.m_curr, c)
        self.goto(cur)
        
    def next(self): 

        c=self.count()
        l=self.m_layout
        cur=l.nextPage(self.m_curr, c)
        self.goto(cur)

    def setPaintLinks(self, cond=True):

        self.m_paintlinks=cond
        for i in self.m_items:
            i.setPaintLinks(cond)
            i.refresh(dropCache=True)

    def paintLinks(self): 
        return self.m_paintlinks
    
    def screenLeft(self, digit=1):
        self.moveScreen('left', digit)
        
    def screenRight(self, digit=1):
        self.moveScreen('right', digit)

    def screenUp(self, digit=1):
        self.moveScreen('up', digit)

    def screenDown(self, digit=1):
        self.moveScreen('down', digit)

    def zoomIn(self, digit=1):
        self.setZoom('in', digit)

    def zoomOut(self, digit=1): 
        self.setZoom('out', digit)
        
    def down(self, digit=1):
        self.move('down', digit)

    def up(self, digit=1):
        self.move('up', digit)

    def left(self, digit=1):
        self.move('left', digit)

    def right(self, digit=1):
        self.move('right', digit)

    def goto(self, *args, **kwargs):
        pass

    def moveScreen(self, kind, digit=1):

        h=self.size().height()
        vbar=self.verticalScrollBar()
        hbar=self.horizontalScrollBar()
        vh=self.m_layout.height(h)
        vw=self.m_layout.height(h)
        sh=self.scene().sceneRect().height()
        sw=self.scene().sceneRect().height()
        if kind=='up':
            dx=vbar.value() - vh*digit
            dx=max(0, dx) 
            vbar.setValue(int(dx))
        elif kind=='down':
            dx=vbar.value() + vh*digit
            dx=min(sh, dx) 
            vbar.setValue(int(dx))
        elif kind=='left':
            dy=hbar.value() - vw*digit
            dy=max(0, dy) 
            hbar.setValue(int(dy))
        elif kind=='right':
            dy=hbar.value() + vw*digit
            dy=min(sw, dy) 
            hbar.setValue(int(dy))
        self.setVisiblePage()

    def setZoom(self, kind='out', digit=1):

        if self.scaleMode() != 'ScaleFactor': 
            self.setScaleMode('ScaleFactor')
        zf = self.zoomFactor
        if kind=='out':
            zf=(1.-zf)**digit
        elif kind=='in':
            zf=(1.+zf)**digit
        x, y = self.getPosition()
        for item in self.m_items: 
            n_zf=zf*item.scale()
            item.setScaleFactor(n_zf)
        self.updateView(x, y)

    def move(self, kind, digit=1):

        s=self.size()
        l=self.m_layout
        sr=self.scene().sceneRect()
        vbar=self.verticalScrollBar()
        hbar=self.horizontalScrollBar()
        vw=l.width(s.width())
        vh=l.height(s.height())
        inc_vh=vh*self.zoomFactor
        inc_vw=vw*self.zoomFactor
        if kind=='down':
            dx=vbar.value() + inc_vh*digit
            dx=min(sr.height(), dx)
            vbar.setValue(int(dx))
        elif kind=='up':
            dx=vbar.value() - inc_vh*digit
            dx=max(0, dx)
            vbar.setValue(int(dx))
        elif kind=='right':
            dx=hbar.value() + inc_vw*digit
            hbar.setValue(int(dx))
        elif kind=='left':
            dx=hbar.value() - inc_vw*digit
            hbar.setValue(int(dx))
        self.setVisiblePage()

    def kind(self):

        if self.m_model:
            return self.m_model.kind()

    def getLocation(self, encode=True):

        if encode:
            x, y = self.getPosition()
            x, y = str(x), str(y)
            return ':'.join([x, y])
        else:
            raise
