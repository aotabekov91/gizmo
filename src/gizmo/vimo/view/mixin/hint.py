from PyQt5 import QtCore

class Hint:

    canHint=True
    hintFinished=QtCore.pyqtSignal()
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    hintSelected=QtCore.pyqtSignal(object)

    def updateHintItems(self):
        pass

    def connectHint(self):
        pass

    def disconnectHint(self):
        pass

    def setup(self):

        self.m_hint_cache={}
        self.m_hinting=False
        self.clearHint()
        super().setup()

    def hint(self, alist=None, kind=None):

        self.m_hinting=True
        if alist:
            m, mm=self.generate(alist)
            self.m_hint_map=m
            self.m_hint_remap=mm
            self.connectHint()
            self.updateHintItems()
        else:
            self.hintFinished.emit()
            self.cleanUpHinting()

    def updateHint(self, key=''):

        match={}
        for k, l in self.m_hint_remap.items():
            if key==k[:len(key)]:
                match[k]=l
        if len(match)==0:
            self.hintFinished.emit()
            self.cleanUpHinting()
            self.disconnectHint()
        elif len(match)==1:
            d=match[list(match.keys())[0]]
            self.hintSelected.emit(d)
            self.cleanUpHinting()
            self.disconnectHint()
        else:
            hints={}
            for k, d in match.items():
                i=d['item']
                if not i  in hints:
                    hints[i]={}
                hints[i][k]=d
            self.m_hint_map=hints
            self.m_hint_remap=match
            self.updateHintItems()

    def cleanUpHinting(self):

        self.m_hinting=False
        self.clearHint()

    def clearHint(self):

        self.m_hint_map={}
        self.m_hint_remap={}

    def generate(self, alist):

        l, hmap, hints, = 0, {}, {}
        al=len(self.alpha)
        ll=len(alist)
        while al**l<ll: l+=1
        l = max(l, 1)
        for j, d in enumerate(alist):
            self.savePointer(j, d, l, hmap, hints)
        return hints, hmap

    def savePointer(self, j, d, l, hmap, hints):

        item=d['item']
        if not item in hints:
            hints[item]={}
        m=self.remap(j, l)
        hints[item][m]=d
        hmap[m]=d

    def remap(self, n, l):

        c = []
        for _ in range(l):
            c.append(self.alpha[n % len(self.alpha)])
            n = n // len(self.alpha)
        return "".join(reversed(c))
