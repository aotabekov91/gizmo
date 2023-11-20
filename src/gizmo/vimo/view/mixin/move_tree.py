from .move_view import ViewMove
from gizmo.utils import tag

class TreeMove(ViewMove):

    @tag('e', modes=['normal|TreeView'])
    def expandAll(self):
        super().expandAll()

    @tag('c', modes=['normal|TreeView'])
    def collapseAll(self):
        super().collapseAll()

    @tag('H', modes=['normal|TreeView'])
    def collapseAllInside(self):
        super().collapseAllInside()

    @tag('d', modes=['normal|TreeView'])
    def rootDown(self, digit=1):
        super().rootDown(digit)

    @tag('u', modes=['normal|TreeView'])
    def rootUp(self, digit=1):
        super().rootUp(digit)
