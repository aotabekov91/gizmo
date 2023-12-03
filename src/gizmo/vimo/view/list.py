from gizmo import widget
from gizmo.vimo.view import mixin

from .base import View 

class ListView(
        mixin.ViewGo,
        View, 
        widget.ListView,
        ):

    def setModel(self, model):

        if model:
            self.m_model
            super().setModel(model)
            super(widget.ListView, self).setModel(model)
