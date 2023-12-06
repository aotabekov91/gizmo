from PyQt5 import QtGui
from .utils import BaseScene

class Scene:

    hasScene=True
    sceneColor='black'
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
            if self.sceneColor:
                s.setBackgroundBrush(
                        QtGui.QColor(self.sceneColor))

    def clearScene(self):

        if self.m_scene:
            self.m_scene.clear()
