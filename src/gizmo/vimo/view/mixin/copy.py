from functools import partial

class Copy:

    canCopy=True

    def copy(self, *args, **kwargs):

        m=self.m_model
        c=self.m_config
        s=self.m_state.copy()
        v=self.app.handler.getView(
                model=m, config=c)
        self.app.handler.setView(v)
        self.app.handler.activateView(
                v, *args, **kwargs)
        v.modelLoaded.connect(
                partial(self.setCopyState, 
                        state=s,
                        copy=v))

    def setCopyState(self, state, copy, **kwargs):
        copy.setStates(state, want=True)
