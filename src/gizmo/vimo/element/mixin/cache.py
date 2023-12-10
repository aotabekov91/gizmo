class Cache:

    canCache=True

    def setup(self):

        super().setup()
        self.m_cache={}

    def addCache(self, name='default', holder={}):

        if not name in self.m_cache:
            self.m_cache[name]=holder

    def dropCache(self, key, name='default'):

        if name in self.m_cache:
            self.m_cache[name].pop(key, None)

    def setCache(self, key, value, name='default'):
        self.m_cache[name][key]=value

    def getCache(self, key, name='default'):
        return self.m_cache[name].get(key, None)

    def clearCache(self, name='default'):

        self.m_cache.pop(name, None)
        self.addCache(name)
