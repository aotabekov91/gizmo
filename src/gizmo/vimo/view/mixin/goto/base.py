from PyQt5 import QtCore

class Go:

    canGo=True
    positionChanged=QtCore.pyqtSignal()
    indexChanged=QtCore.pyqtSignal(object)

    def go(self, kind='', *args, **kwargs):

        k=''
        if kind: k=kind[0].title()+kind[1:]
        f=getattr(self, f'goTo{k}', None)
        if f: f(*args, **kwargs)
