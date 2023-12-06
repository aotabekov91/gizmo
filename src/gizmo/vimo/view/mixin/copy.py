class Copy:

    canCopy=True

    def copy(self, *args, **kwargs):

        m=self.m_model
        c=self.m_config
        s=self.m_state.copy()
        v=self.app.handler.getView(
                state=s,
                model=m,
                config=c,
                )
        self.app.handler.setView(v)
        self.app.handler.activateView(
                v, *args, **kwargs)
        v.setStates(s)
