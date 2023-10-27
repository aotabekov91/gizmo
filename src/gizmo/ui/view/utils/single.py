class SinglePage:

    def __init__(self, config):

        self.config=config
        self.viewportPadding=config.get('viewportPadding', 0) 

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

        ps=self.config.get('pageSpacing', 0.0)
        return width-self.viewportPadding-2.*ps

    def height(self, height):

        ps=self.config.get('pageSpacing', 0.0)
        return height-2.0*ps

    def load(
            self, 
            items, 
            left, 
            right, 
            height,
            rightToLeft, 
            ):

        ps=self.config.get('pageSpacing', 0.0)
        ph=0.
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
