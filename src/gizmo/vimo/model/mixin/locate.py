class Locate:

    canLocate=True
    
    def findLocator(self, prefix, kind):

        if kind:
            n=f'{prefix}{kind.title()}Locator'
            return getattr(self, n, None)

    def delLocator(self, data=None, kind=None):

        f=self.findLocator('del', kind)
        if f: return f(data)
        return {}

    def getLocator(self, data=None, kind=None):

        f=self.findLocator('get', kind)
        if f: return f(data)
        return {}
    
    def getUniqLocator(self, data=None, kind=None):

        f=self.findLocator('getUniq', kind)
        if f: return f(data)
        return {}

    def setLocator(self, data=None, kind=None):

        f=self.findLocator('set', kind)
        if f: return f(data)
        return {}

    def openLocator(self, data=None, kind=None):

        f=self.findLocator('open', kind)
        if f: return f(data)
        return {}
