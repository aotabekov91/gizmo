class Dir:

    def setModel(self, model):

        super().setModel(model)
        self.jumpToSource()

    def jumpToSource(self):

        e=self.m_model.sourceElement()
        for i, j in self.m_items.items():
            if j.element()==e:
                return self.goTo(i)
