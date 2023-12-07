from .base import Fullscreen

class TFullscreen(Fullscreen):

    isFullscreen=False 
    canFullscreen=True

    def toggleFullscreen(self):

        if self.isFullscreen:
            idx=self.m_tab_idx
            p=self.m_parent_tab
            p.insertWidget(idx, self)
            self.isFullscreen=False
            p.tabSet(self)
            p.setFocus()
        else:
            p=self.parent()
            self.m_parent_tab=p
            p.removeWidget(self)
            self.setParent(self.app.ui.overlay)
            self.resize(self.app.ui.overlay.size())
            self.isFullscreen=True
            self.show()
