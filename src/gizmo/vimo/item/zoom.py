class Zoom:

    canZoom=True

    def setup(self):

        super().setup()
        self.scale=self.kwargs.get(
                'scaleFactor', .1)

    def setZoomFactor(self, zfactor):

        self.scale=zfactor
        self.redraw(refresh=True)
