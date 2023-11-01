from PyQt5 import QtCore, QtGui

class BaseItem:

    wasModified = QtCore.pyqtSignal()
    mouseDoubleClick=QtCore.pyqtSignal(
            int, object)
    mouseReleaseOccured=QtCore.pyqtSignal(
            object, object)
    mouseMoveOccured=QtCore.pyqtSignal(
            object, object)
    mousePressOccured=QtCore.pyqtSignal(
            object, object)
    hoverMoveOccured=QtCore.pyqtSignal(
            object, object)
    mouseDoubleClickOccured=QtCore.pyqtSignal(
            object, object)

    def __init__(
            self, 
            cache={},
            config={},
            size=None,
            trans = QtGui.QTransform(),
            index=None,
            rotation=0,
            searched=[],
            element=None,
            xresol=72,
            yresol=72,
            useTiling=False,
            scaleFactor=1.,
            proxyPadding=0.,
            devicePixelRatio=1.,
            norm = QtGui.QTransform(),
            **kwargs
            ):

        self.m_id=index
        self.m_size=size
        self.m_cache=cache
        self.m_searched=[]
        self.m_norm = norm 
        self.m_config=config
        self.m_trans = trans
        self.rotation=rotation
        self.scale=scaleFactor
        self.m_element = element
        self.proxyPadding=proxyPadding
        self.devicePixelRatio=devicePixelRatio
        self.xresol=xresol
        self.yresol=yresol
        self.m_paint_links=False
        self.useTiling=useTiling
        self.m_brect = QtCore.QRectF() 
        self.select_pcolor=QtCore.Qt.red
        self.select_bcolor=QtGui.QColor(
                88, 139, 174, 30)
        super().__init__(**kwargs)
        self.setup()
        self.initialize()

    def setSearched(self, searched=[]): 
        self.m_searched=searched

    def size(self):
        return self.m_size

    def initialize(self):
        pass

    def refresh(self, *args, **kwargs):
        pass

    def redraw(self, *args, **kwargs):
        pass

    def mapToElement(self, *args, **kwargs):
        pass

    def mapToItem(self, *args, **kwargs):
        pass

    def showOverlay(self, *args, **kwargs):
        pass
    
    def hideOverlay(self, *args, **kwargs):
        pass

    def addProxy(self, *args, **kwargs):
        pass

    def prepareProxyGeometry(self, *args, **kwargs):
        pass

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickOccured.emit(self, event)

    def mousePressEvent(self, event):
        self.mousePressOccured.emit(self, event)

    def mouseMoveEvent(self, event):
        self.mouseMoveOccured.emit(self, event)

    def mouseReleaseEvent(self, event):
        self.mouseReleaseOccured.emit(self, event)

    def hoverMoveEvent(self, event):
        self.hoverMoveOccured.emit(event, self)

    def setScaleFactor(self, factor):

        self.scale=factor
        self.redraw(refresh=True)

    def setSettings(self):

        c=self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setup(self):
        self.setSettings()

    def select(self, *args, **kwargs):
        pass

    def index(self):
        return self.m_id

    def setIndex(self, idx):
        self.m_id=idx

    def element(self): 
        return self.m_element
