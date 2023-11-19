from gizmo.utils import tag

from .go import Go

class TreeGo(Go):

    def go(self, kind, *args, **kwargs):

        if type(kind)==int:
            self.goto(kind)
        elif kind=='first':
            self.gotoFirst()
        elif kind=='last':
            self.gotoLast()

    @tag('gf', modes=['normal|TreeView'])
    def gotoFirstSibling(self): 
        super().gotoFirstSibling()

    @tag('gl', modes=['normal|TreeView'])
    def gotoLastSibling(self): 
        super().gotoLastSibling()

    @tag('gp', modes=['normal|TreeView'])
    def gotoParent(self):
        super().gotoParent()

    @tag('gs', modes=['normal|TreeView'])
    def gotoSiblingDown(self, digit=1):
        super().gotoSiblingDown(digit)

    @tag('gS', modes=['normal|TreeView'])
    def gotoSiblingUp(self, digit=1):
        super().gotoSiblingUp()
