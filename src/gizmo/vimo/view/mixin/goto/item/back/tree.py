from gizmo.utils import tag

from .view import ViewGo

class TreeGo(ViewGo):

    @tag('gf', modes=['normal|TreeView'])
    def goToFirstSibling(self): 
        super().gotoFirstSibling()

    @tag('gl', modes=['normal|TreeView'])
    def goToLastSibling(self): 
        super().gotoLastSibling()

    @tag('gp', modes=['normal|TreeView'])
    def goToParent(self):
        super().gotoParent()

    @tag('gs', modes=['normal|TreeView'])
    def goToSiblingDown(self, digit=1):
        super().gotoSiblingDown(digit)

    @tag('gS', modes=['normal|TreeView'])
    def goToSiblingUp(self, digit=1):
        super().gotoSiblingUp()

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
