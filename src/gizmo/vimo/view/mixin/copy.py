class Copy:

    canCopy=True

    def copy(self, *args, **kwargs):

        m=self.m_model
        c=self.m_config
        v=self.app.handler.getView(
                self.m_model, config=self.m_config)
        self.app.handler.setView(v)
        self.app.handler.activateView(
                v, *args, **kwargs)
