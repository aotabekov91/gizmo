from PyQt5 import QtCore

class Go:

    canGo=True
    positionChanged=QtCore.pyqtSignal()
    indexChanged=QtCore.pyqtSignal(object)

    def go(
           self, 
           *args, 
           kind='', 
           mode='', 
           **kwargs
           ):

        k=''
        if kind: k=kind[0].title()+kind[1:]
        n=f'goTo{k}'
        if mode: n=mode+n[0].title()+n[1:]
        f=getattr(self, n,  None)
        if f: f(*args, **kwargs)
