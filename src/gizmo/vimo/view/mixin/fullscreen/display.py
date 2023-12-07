from .base import Fullscreen

class DFullscreen(Fullscreen):

    isFullscreen=False 
    canFullscreen=True

    def toggleFullscreen(self, view=None):

        if self.isFullscreen:
            self.hide()
            self.isFullscreen=False
            p=self.m_parent_tab
            p.setView(self)
            self.setFocus()
        else:
            p=self.parent()
            o=self.app.ui.overlay
            self.isFullscreen=True
            self.m_parent_tab=p
            cr, pr = p.closeView(self)
            self.m_prev_view=pr
            self.setParent(o)
            self.setGeometry(o.geometry())
            self.show()
            self.setFocus()
