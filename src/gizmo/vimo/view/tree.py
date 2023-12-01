from gizmo import widget

from .base import View 

class TreeView(View, widget.TreeView):

    def setModel(self, model):

        if model:
            self.m_model
            super().setModel(model)
            super(widget.TreeView, self).setModel(model)
