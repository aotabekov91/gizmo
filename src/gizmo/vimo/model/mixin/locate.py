from gizmo.utils import hashabledict

class Locate:

    canLocate=True

    def createLocator(self, data={}):
        return hashabledict(data)
    
    def findLocator(self, prefix, kind):

        if kind:
            n=f'{prefix}{kind.title()}Locator'
            return getattr(self, n, None)

    def delLocator(self, data={}, kind=None):

        f=self.findLocator('del', kind)
        if f: return f(data)
        return self.createLocator(data)

    def getLocator(self, data={}, kind=None):

        f=self.findLocator('get', kind)
        if f: return f(data)
        return self.createLocator(data)
    
    def getUniqLocator(self, data={}, kind=None):

        f=self.findLocator('getUniq', kind)
        if f: return f(data)
        return self.createLocator(data)

    def setLocator(self, data={}, kind=None):

        f=self.findLocator('set', kind)
        if f: return f(data)
        return self.createLocator(data)

    def openLocator(self, data={}, kind=None):

        f=self.findLocator('open', kind)
        if f: return f(data)
        return self.createLocator(data)
