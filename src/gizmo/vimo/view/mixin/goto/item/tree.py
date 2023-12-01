from gizmo.utils import tag

from .view import ViewGo

class TreeGo(ViewGo):

    def goToLast(self):
        self.goToLastSibling()

    def getRowIndex(self, row):

        idx=self.currentIndex()
        pidx=idx.parent()
        return pidx.child(row, 0) 

    def goToRight(self, *args, **kwargs):
        super().expand()

    def goToLeft(self, *args, **kwargs):
        super().collapse()

    @tag('gf', modes=['normal|TreeView'])
    def goToFirstSibling(self): 
        super().goToFirstSibling()

    @tag('gl', modes=['normal|TreeView'])
    def goToLastSibling(self): 
        super().goToLastSibling()

    @tag('gp', modes=['normal|TreeView'])
    def goToParent(self):
        super().goToParent()

    @tag('gs', modes=['normal|TreeView'])
    def goToSiblingDown(self, digit=1):
        super().goToSiblingDown(digit)

    @tag('gS', modes=['normal|TreeView'])
    def goToSiblingUp(self, digit=1):
        super().goToSiblingUp()

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
