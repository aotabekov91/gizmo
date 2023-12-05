from .leaf import Leaf

class TileLayout:

    def __init__(self, parent=None):

        self.delta=10
        self.ratio=1.6
        self.root = Leaf()
        self.parent=parent
        self.lower_right=True
        self.current = self.root

    def count(self):

        widgets = list(self.root.widgets())
        return len(widgets)

    def getLeaf(self, widget):

        for leaf in self.root:
            if widget is leaf.widget: 
                return leaf

    def focusLeaf(self, leaf):

        if leaf:
            self.current=leaf
            if leaf.widget: 
                leaf.widget.setFocus()

    def focusWidget(self, widget):

        if widget:
            leaf=self.getLeaf(widget)
            self.focusLeaf(leaf)
            return leaf

    def addWidget(
            self, 
            widget, 
            horizontal=True, 
            **kwargs):

        l = self.current
        l.horizontal=horizontal
        widget.setParent(self.parent)
        self.current = l.insert(
                widget,
                int(self.lower_right), 
                self.ratio)
        self.update()

    def clear(self):

        for w in self.root.widgets():
            self.removeWidget(w)

    def removeWidget(self, widget):

        leaf = self.getLeaf(widget)
        widget.hide()
        if leaf:
            if leaf.parent:
                leaf = leaf.parent.remove(leaf)
                newwidget = next(leaf.widgets(), None)
                if newwidget is None:
                    self.current = self.root
                else:
                    self.current = self.getLeaf(newwidget)
                if leaf.parent: 
                    leaf.parent.update()
                else:
                    self.root.update()
                return (newwidget, widget)
            leaf.widget = None
            self.current = self.root
        return (None, widget)

    def update(self):

        r=self.parent.rect()
        x, y = r.x(), r.y()
        w, h = r.width(), r.height()
        self.root.calc_geom(x, y, w, h)

    def toggleSplit(self):

        if self.current.parent:
            cond = self.current.parent.horizontal
            self.current.parent.horizontal = not cond
            self.update()

    def findSibling(self, widget, kind='next'):

        widgets = list(self.root.widgets())
        if widget in widgets:
            idx = widgets.index(widget)
            if kind=='next':
                idx=min(len(widgets)-1, idx+1)
            if kind=='prev':
                idx=max(0, idx-1)
            return widgets[(idx)]

    def findLeaf(self, d):

        l = self.current
        p = l.parent
        while p:
            x, y  = self.current.x, self.current.y
            w, h =  self.current.w, self.current.h
            if d=='up':
                if p.horizontal and l is p.leaves[1]:
                    n_ = p.leaves[0]
                    center = x + w * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].x < center
                        if not n_.horizontal or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif d=='down':
                if p.horizontal and l is p.leaves[0]:
                    n_ = p.leaves[1]
                    center = x + w * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].x > center
                        if not n_.horizontal or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            elif d=='left':
                if not p.horizontal and l is p.leaves[1]:
                    n_ = p.leaves[0]
                    center = y + h * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].y < center
                        if n_.horizontal or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif d=='right':
                if not p.horizontal and l is p.leaves[0]:
                    n_ = p.leaves[1]
                    center = y + h * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].y > center
                        if n_.horizontal or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            l = p
            p = l.parent

    def equalize(self):

        cond = False
        for n in self.root:
            if n.ratio != 50:
                n.ratio = 50
                cond = True
        if cond:
            self.root.equalize()
            self.update()

    def goTo(self, kind, digit=1):

        pos=['right', 'left', 'down', 'up']
        if digit is not None:
            digit-=1
            widgets = list(self.root.widgets())
            if 0<=digit<len(widgets):
                w=widgets[digit]
                return self.focusWidget(w)
        elif kind in pos:
            leaf = self.findLeaf(kind)
            self.focusLeaf(leaf)
            return leaf
        elif kind == 'next':
            w = self.findSibling(
                    self.current.widget, 'next')
            return self.focusWidget(w)
        elif kind == 'prev':
            w = self.findSibling(
                    self.current.widget, 'prev')
            return self.focusWidget(w)
        elif kind == 'first':
            w=next(self.root.widgets(), None)
            return self.focusWidget(w)
        elif kind == 'last':
            widgets = list(self.root.widgets())
            w = widgets[-1] if len(widgets) else None
            return self.focusWidget(w)

    def move(self, kind=None, digit=None):

        leaf=None
        if not digit is None:
            digit-=1
            widgets = list(self.root.widgets())
            if 0<=digit<len(widgets):
                w=widgets[digit]
                leaf=self.getLeaf(w)
        else:
            leaf = self.findLeaf(kind)
        if leaf:
            nw, cw= self.current.widget, leaf.widget
            leaf.widget, self.current.widget = nw, cw
            self.current = leaf
            self.update()
        elif self.current is not self.root:
            leaf = self.current
            self.removeWidget(leaf.widget)
            newroot = Leaf()
            if kind in ['up', 'down']:
                newroot.horizontal = True
                newroot.leaves = [self.root, leaf]
            elif kind in ['left', 'right']:
                newroot.horizontal = False
                newroot.leaves = [leaf, self.root]
            self.root.parent = newroot
            leaf.parent = newroot
            self.root = newroot
            self.current = leaf
            self.update()

    def flip(self, d):

        l = self.current
        p = l.parent
        while p:
            c = not p.horizontal
            if d in ['left', 'right']:
                c = p.horizontal
            cond = c and l is p.leaves[0]
            if d in ['left', 'up']:
                cond = c and l is p.leaves[1]
            if cond:
                p.leaves = p.leaves[::-1]
                self.update()
                break
            l = p
            p = l.parent

    def resize(self, d, k='increment'):

        l = self.current
        p = l.parent
        while p:
            cond = not p.horizontal
            if d in ['left', 'right']: 
                cond = p.horizontal
            if d in ['right', 'down']:
                cond = cond and l is p.leaves[0]
                ratio=max(5, p.ratio - self.delta)
                if k=='increment':
                    ratio = min(95, p.ratio + self.delta)
            elif d in ['left', 'up']:
                cond = cond and l is p.leaves[1]
                ratio=min(95, p.ratio + self.delta)
                if k=='increment':
                    ratio = max(5, p.ratio - self.delta)
            if cond:
                p.ratio = ratio
                p.update()
                break
            l = p
            p = l.parent
