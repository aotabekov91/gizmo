from gizmo.vimo.view import mixin
from gizmo.widget import ListView as List

from .base import View 

class ListView(
        mixin.ViewGo,
        View, 
        List,
        ):

    def setModel(self, model):

        if model:
            self.m_model
            super().setModel(model)
            super(List, self).setModel(model)
