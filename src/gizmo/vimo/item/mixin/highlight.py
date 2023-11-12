from PyQt5 import QtGui

class Highlight:

    canHighlight=True
    def setup(self):

        self.color_alpha=50
        self.pen_thickness=10
        self.m_highlighted=None
        self.highlight_color='yellow'
        super().setup()
        self.highlight_color=QtGui.QColor(
                self.highlight_color)
        self.highlight_color.setAlpha(
                self.color_alpha)
        self.m_pen=QtGui.QPen(
                self.highlight_color,
                self.pen_thickness)
        self.m_brush=QtGui.QBrush(
                self.highlight_color)
        self.painted.connect(
                self.paintHighlight)

    def highlighted(self):
        return self.m_highlighted

    def highlight(self, h):

        self.m_highlighted=h
        self.update()

    def paintHighlight(self, p, o, w, i):

        if self.m_highlighted:
            p.save()
            box=self.m_highlighted.get('box', [])
            for s in box:
                p.setPen(self.m_pen)
                p.setBrush(self.m_brush)
                s=self.mapToItem(s, unified=True)
                p.drawRects(s)
            p.restore()
