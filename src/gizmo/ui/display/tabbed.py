from gizmo.vimo import view
from gizmo.utils import tag

from .tiled import TileDisplay

class TabbedTileDisplay(view.Tabber):

    tab_class=TileDisplay

    def __init__(
            self, 
            app=None,
            window=None, 
            **kwargs):

        super().__init__(
                app=app, 
                parent=window.main,
                **kwargs,
                )
        self.m_window=window
        window.resized.connect(self.update)
        self.show()

    def newTab(self):

        ctab=self.m_current_tab
        if ctab:
            v=ctab.currentView()
            ntab=self.createTab()
            m=v.model()
            s=m.source()
            c=self.app.handler.handleOpen(
                    source=s,
                    config=m.m_config
                    )

    def update(self):

        if self.m_current_tab:
            self.m_current_tab.update()

    def setup(self):

        super().setup()
        self.setupCurrent()

    def setupCurrent(self):

        d=self.getTab()
        self.addTab(d)
        self.setTab(d)

    def setupView(self, view, *args, **kwargs):
        
        if self.m_current_tab:
            self.m_current_tab.setupView(
                    view, *args, **kwargs)
            view.m_tabber=self
            view.hasTabber=True
            view.setParent(
                    self.m_current_tab)
            self.setFocus()

    def setFocus(self):

        super().setFocus()
        c=self.m_current_tab
        if c: 
            c.update()
            c.show()
            c.setFocus() 
            v=c.currentView()
            v.setFocus()
