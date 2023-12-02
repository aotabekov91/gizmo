class Select:

    canSelect=True

    def setup(self):

        self.m_selection=None
        super().setup()

    def select(self, i, s, **kwargs):

        if self.check('canSelect', i):
            i.select(s, **kwargs)
            self.m_selection=s

    def selection(self):
        return self.m_selection

    def clearSelection(self):

        for i in self.m_items.values():
            if self.check('canSelect', i):
                i.select()

    def cleanUp(self):

        super().cleanUp()
        self.clearSelection()
        self.m_selection=None
