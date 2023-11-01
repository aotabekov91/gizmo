class OverlayMixin:

    def showOverlay(
            self, 
            overlay, 
            hideOverlay, 
            elements, 
            selectedElement
            ):

        for e in elements:
            if not e in overlay:
                self.addProxy(overlay, hideOverlay, e)
            if e==selectedElement:
                overlay[e].widget().setFocus()

    def hideOverlay(
            self, 
            overlay, 
            deleteLater=False
            ):

        dover=Overlay()
        dover.swap(overlay)
        if not dover.isEmpty():
            for i in range(dover.constEnd()):
                if deleteLater: 
                    raise
            self.refresh()

    def addProxy(
            self, 
            pos, 
            wid, 
            hideOverlay
            ):

        p=QtWidgets.QGraphicsProxyWidget(self)
        p.setWidget(wid)
        wid.setFocus()
        p.setAutoFillBackground(True)
        self.setProxyGeometry(pos, p)
        p.visibleChanged.connect(hideOverlay)
