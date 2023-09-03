from .node import Node

class TileLayout:

    def __init__(self, parent):

        self.delta=10
        self.ratio=1.6
        self.root = Node()
        self.parent=parent
        self.lower_right=True
        self.current = self.root

    def getNode(self, widget):

        for n in self.root:
            if widget is n.widget: return n

    def focusNode(self, node):

        if node:
            self.current=node
            if node.widget: 
                node.widget.setFocus()

    def focusWidget(self, widget):

        if widget:
            node=self.getNode(widget)
            self.focusNode(node)
            return node

    def addWidget(self, widget, hsplit=False):

        node = self.current
        node.hsplit=hsplit
        widget.setParent(self.parent)
        self.current = node.insert(
                widget, 
                int(self.lower_right), 
                self.ratio)
        self.update()

    def clear(self):

        for w in self.root.widgets():
            self.removeWidget(w)

    def removeWidget(self, widget):

        node = self.getNode(widget)
        widget.hide()
        if node:
            if node.parent:
                node = node.parent.remove(node)
                newwidget = next(node.widgets(), None)
                if newwidget is None:
                    self.current = self.root
                else:
                    self.current = self.getNode(newwidget)
                if node.parent: 
                    node.parent.update()
                else:
                    self.root.update()
                return (newwidget, widget)
            node.widget = None
            self.current = self.root
        return (None, widget)

    def update(self):

        screen_rect=self.parent.rect()
        self.root.calc_geom(
                screen_rect.x(),
                screen_rect.y(),
                screen_rect.width(), 
                screen_rect.height())

    def toggleSplit(self):

        if self.current.parent:
            cond = self.current.parent.hsplit
            self.current.parent.hsplit = not cond
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

    def findNode(self, d):

        l = self.current
        p = l.parent
        while p:
            x, y  = self.current.x, self.current.y
            w, h =  self.current.w, self.current.h
            if d=='up':
                if not p.hsplit and l is p.leaves[1]:
                    n_ = p.leaves[0]
                    center = x + w * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].x < center
                        if not n_.hsplit or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif d=='down':
                if not p.hsplit and l is p.leaves[0]:
                    n_ = p.leaves[1]
                    center = x + w * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].x > center
                        if not n_.hsplit or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            elif d=='left':
                if p.hsplit and l is p.leaves[1]:
                    n_ = p.leaves[0]
                    center = y + h * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].y < center
                        if n_.hsplit or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif d=='right':
                if p.hsplit and l is p.leaves[0]:
                    n_ = p.leaves[1]
                    center = y + h * 0.5
                    while n_.widget is None:
                        c = n_.leaves[1].y > center
                        if n_.hsplit or c:
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

    def focus(self, kind):

        pos=['right', 'left', 'down', 'up']
        if kind in pos:
            node = self.findNode(kind)
            self.focusNode(node)
            return node
        elif kind == 'next':
            widget = self.findSibling(
                    self.current.widget, 'next')
            return self.focusWidget(widget)
        elif kind == 'prev':
            widget = self.findSibling(
                    self.current.widget, 'prev')
            return self.focusWidget(widget)
        elif kind == 'first':
            widget=next(self.root.widgets(), None)
            return self.focusWidget(widget)
        elif kind == 'last':
            widgets = list(self.root.widgets())
            widget = widgets[-1] if len(widgets) else None
            return self.focusWidget(widget)

    def move(self, d):

        node = self.findNode(d)
        if node:
            nw, cw= self.current.widget, node.widget
            node.widget, self.current.widget = nw, cw
            self.current = node
            self.update()
        elif self.current is not self.root:
            node = self.current
            self.removeWidget(node.widget)
            newroot = Node()

            newroot.hsplit = True
            if d in ['up', 'down']:
                newroot.hsplit = False

            newroot.leaves = [self.root, node]
            if d in ['left', 'up']:
                newroot.leaves = [node, self.root]

            self.root.parent = newroot
            node.parent = newroot
            self.root = newroot
            self.current = node
            self.update()

    def flip(self, d):

        l = self.current
        p = l.parent
        while p:
            c = not p.hsplit
            if d in ['left', 'right']:
                c = p.hsplit
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

            cond = not p.hsplit
            if d in ['left', 'right']: 
                cond = p.hsplit

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
