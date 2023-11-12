class Locate:

    def findLocator(self, prefix, kind):

        if kind:
            n=f'{prefix}{kind.title()}Locator'
            return getattr(self, n, None)

    def delLocator(self, data=None, kind=None):

        f=self.findLocator('del', kind)
        if f: return f(data)
        return self.m_model.delLocator(
                data=data, kind=kind)

    def getLocator(self, data=None, kind=None):

        f=self.findLocator('get', kind)
        if f: return f(data)
        return self.m_model.getLocator(
                data=data, kind=kind)

    def getUniqLocator(self, data=None, kind=None):

        f=self.findLocator('getUniq', kind)
        if f: return f(data)
        return self.m_model.getUniqLocator(
                data=data, kind=kind)

    def setLocator(self, data=None, kind=None):

        f=self.findLocator('set', kind)
        if f: return f(data)
        return self.m_model.setLocator(
                data=data, kind=kind)

    def openLocator(self, data=None, kind=None):

        f=self.findLocator('open', kind)
        if f: return f(data)
        return self.m_model.openLocator(
                data=data, kind=kind)
