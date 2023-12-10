from PyQt5 import QtGui
from .utils import BaseScene

from ..layout import Layout

class Scene(Layout):

    hasScene=True
    scene_color='black'
    scene_class=BaseScene

    def setup(self):

        self.m_scene=None
        super().setup()
        self.setupScene()

    def setupScene(self):

        if self.scene_class:
            s=self.scene_class()
            self.m_scene=s
            self.setScene(s)
            if self.scene_color:
                c=QtGui.QColor(self.scene_color)
                s.setBackgroundBrush(c)

    def clearScene(self):
        self.m_scene.clear()

    def redrawScene(self):

        l, r, h = self.m_layout.load(
                self.m_items)
        self.m_scene.setSceneRect(
                l, 0.0, r-l, h)
