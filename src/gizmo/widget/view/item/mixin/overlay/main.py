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

    def setProxyGeometry(self, pos, proxy):

        width=proxy.preferredWidth()
        height=proxy.preferredHeight()
        x=pos.x()-0.5*proxy.preferredWidth()
        y=pos.y()-0.5*proxy.preferredHeight()
        proxyPadding=self.proxyPadding
        x=max([x, self.m_brect.left()+proxyPadding])
        y=max([y, self.m_brect.top()+ proxyPadding])
        width=min([width, self.m_brect.right()-proxyPadding-x])
        height=min([height, self.m_brect.bottom()-y])
        proxy.setGeometry(
                QtCore.QRectF(x, y, width, height))
