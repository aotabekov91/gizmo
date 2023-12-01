from .view import ViewGo

class SceneGo(ViewGo):

    def goToNext(self, *args, **kwargs):
        self.nextItem(*args, **kwargs)

    def goToPrev(self, *args, **kwargs):
        self.prevItem(*args, **kwargs)

    def goToScreenLeft(self, digit=1):
        self.moveScreen('left', digit)
        
    def goToScreenRight(self, digit=1):
        self.moveScreen('right', digit)

    def goToScreenUp(self, digit=1):
        self.moveScreen('up', digit)

    def goToScreenDown(self, digit=1):
        self.moveScreen('down', digit)

    def goToDown(self, digit=1):
        self.move('down', digit)

    def goToUp(self, digit=1):
        self.move('up', digit)

    def goToLeft(self, digit=1):
        self.move('left', digit)

    def goToRight(self, digit=1):
        self.move('right', digit)

    def goToLast(self):
        self.goTo(self.count())

    def moveScreen(self, kind, digit=1):

        s=self.size()
        h, w=s.height(), s.width()
        sr=self.scene().sceneRect()
        sh, sw = sr.height(), sr.width()
        vb=self.verticalScrollBar()
        hb=self.horizontalScrollBar()
        if self.check('hasLayout'):
            h=self.m_layout.height(h)
            w=self.m_layout.height(w)
        if kind=='up':
            dx=vb.value() - h*digit
            dx=max(0, dx) 
            vb.setValue(int(dx))
        elif kind=='down':
            dx=vb.value() + h*digit
            dx=min(sh, dx) 
            vb.setValue(int(dx))
        elif kind=='left':
            dy=hb.value() - w*digit
            dy=max(0, dy) 
            hb.setValue(int(dy))
        elif kind=='right':
            dy=hb.value() + w*digit
            dy=min(sw, dy) 
            hb.setValue(int(dy))
        self.setVisibleItem()
        self.positionChanged.emit()

    def move(self, kind, digit=1):

        s=self.size()
        h, w=s.height(), s.width()
        sr=self.scene().sceneRect()
        vb=self.verticalScrollBar()
        hb=self.horizontalScrollBar()
        if self.check('hasLayout'):
            h=self.m_layout.height(h)
            w=self.m_layout.height(w)
        h=h*self.zoomFactor
        w=w*self.zoomFactor
        if kind=='down':
            dx=vb.value() + h*digit
            dx=min(sr.height(), dx)
            vb.setValue(int(dx))
        elif kind=='up':
            dx=vb.value() - h*digit
            dx=max(0, dx)
            vb.setValue(int(dx))
        elif kind=='right':
            dx=hb.value() + w*digit
            hb.setValue(int(dx))
        elif kind=='left':
            dx=hb.value() - w*digit
            hb.setValue(int(dx))
        self.setVisibleItem()
        self.positionChanged.emit()
