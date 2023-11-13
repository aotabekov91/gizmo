class Copy:

    canCopy=True

    def copy(self):

        s=self.m_model.source()
        for r in self.app.renders:
            if not r.isCompatible(s):
                continue
            return r, r.getView(self.m_model)
