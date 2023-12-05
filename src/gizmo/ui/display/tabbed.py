from gizmo.vimo import view

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

    def setup(self):

        super().setup()
        self.tabAddNew(emit=False)

    def update(self):

        if self.current_tab:
            self.current_tab.update()

    def tabMove(self, kind=None, digit=None):

        c = not digit is None
        if kind == 'moveTo' and c:
            idx=max(0, digit-1)
            c=self.current_tab
            n=self.widget(idx)
            if c and n:
                v=c.closeView()
                n.setupView(view=v)
                if c.count()==0:
                    self.tabClose(c)
                self.tabSet(n)
                self.setFocus()
        else:
            super().tabMove(
                    kind=kind, digit=digit)

    def tabAddNew(self, copy=False, emit=True):

        ctab=self.current_tab
        super().tabAddNew()
        if copy:
            v=ctab.currentView()
            m=v.model()
            s=m.source()
            self.app.handler.handleOpen(
                    source=s,
                    config=m.m_config)
        elif emit:
            self.app.handler.viewChanged.emit(
                    self)

    def setupView(self, view, *args, **kwargs):
        
        if self.current_tab:
            self.current_tab.setupView(
                    view, *args, **kwargs)
            view.m_tabber=self
            view.hasTabber=True
            view.setParent(
                    self.current_tab)
            self.setFocus()

    def currentView(self):

        c=self.current_tab
        if c: return c.currentView()
