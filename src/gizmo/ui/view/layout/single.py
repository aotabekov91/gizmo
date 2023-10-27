class SinglePage:

    def __init__(
            self, 
            config={},
            pageSpacing=0,
            viewportPadding=0,
            **kwargs,
            ):

        self.m_config=config
        self.pageSpacing=pageSpacing
        self.viewportPadding=viewportPadding
        self.setSettings()

    def setSettings(self):

        c=self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def left(self, idx, count=None): 
        return idx

    def right(self, idx, count=None): 
        return idx

    def up(self, idx, count=None): 
        return idx

    def down(self, idx, count=None): 
        return idx

    def next(self, idx, count=None): 
        return min(idx+1, count)

    def prev(self, idx, count=None): 
        return max(idx-1, 1)

    def current(self, idx, count=None): 
        return idx

    def width(self, width):

        ps=self.pageSpacing
        return width-self.viewportPadding-2.*ps

    def height(self, height):
        return height-2.0*self.pageSpacing

    def load(
            self, 
            items, 
            left, 
            right, 
            height,
            rightToLeft, 
            ):

        ph=0.
        ps=self.pageSpacing
        for i in items:
            br=i.boundingRect()
            left=-br.left()-0.5*br.width()
            t=height-br.top()
            i.setPos(left, t)
            ph=br.height()
            left=min(left, -0.5*br.width())#-pageSpacing)
            right=max(right, 0.5*br.width())#+pageSpacing)
            height+=ps+ph
        return left, right, height
