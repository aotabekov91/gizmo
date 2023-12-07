from gizmo.vimo import view

from .tiled import TileDisplay

class TabbedTileDisplay(view.Tabber):

    canFullscreen=True
    tab_class=TileDisplay

    def __init__(
            self, 
            app=None,
            window=None, 
            **kwargs
            ):

        super().__init__(
                app=app, 
                parent=window.main,
                objectName='DisplayView',
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

    def tabMove(
            self, 
            kind=None, 
            digit=None,
            ttab=None,
            ftab=None,
            view=None,
            ):

        if kind == 'moveTo':
            if not ttab:
                idx=max(0, digit-1)
                ttab=self.widget(idx)
            if not ftab:
                ftab=self.current_tab
            if ftab and ttab:
                view=ftab.closeView(view)
                ttab.setupView(view=view)
                if ftab.count()==0:
                    self.tabClose(ftab)
                self.tabSet(ttab)
                self.setFocus()
            return view
        else:
            super().tabMove(
                    kind=kind, digit=digit)

    def tabAddNew(self, copy=False, emit=True):

        ctab=self.current_tab
        ntab=super().tabAddNew()
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
        return ntab

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

    # def toggleFullscreen(self, view=None):

    #     t=self.current_tab
    #     v = view or self.currentView()
    #     if not v: return
    #     c=getattr(v, 'm_fullscreen', False)
    #     if c: 
    #         if t.count()!=1: return 
    #         v.m_fullscreen=False
    #         p=v.m_prev_tab
    #         digit=p.m_tab_idx+1
    #         self.tabMove(
    #                 digit=digit,
    #                 kind='moveTo')
    #         # p.move(leaf=v.m_prev_leaf)
    #     else: 
    #         if t.count()<=1: return
    #         v.m_prev_tab=t
    #         v.m_fullscreen=True
    #         prev=t.m_layout.findSibling(v, kind='prev')
    #         v.m_prev_leaf=t.m_layout.getLeaf(prev)
    #         ttab=self.tabAddNew()
    #         digit=ttab.m_tab_idx+1
    #         self.tabMove(
    #                 ftab=t,
    #                 view=v,
    #                 digit=digit,
    #                 kind='moveTo',
    #                 )
