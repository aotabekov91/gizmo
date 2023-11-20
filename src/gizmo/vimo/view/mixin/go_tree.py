from gizmo.utils import tag

from .go_view import ViewGo

class TreeGo(ViewGo):

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
