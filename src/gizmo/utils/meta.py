from PyQt5 import QtCore
from gizmo.utils.ear import Ear
from gizmo.utils.cfman import CFMan

class MetaKey(type(QtCore.QObject)):

    def __call__(cls, *args, **kwargs):

        obj=type.__call__(cls, *args, **kwargs)
        obj.name=obj.__class__.__name__
        kwargs=getattr(obj, 'kwargs', {})
        obj.ear=Ear(obj=obj, **kwargs)
        obj.ear.listen()
        return obj

class MetaConf(type(QtCore.QObject)):

    def __call__(cls, *args, **kwargs):

        obj=type.__call__(cls, *args, **kwargs)
        obj.name=obj.__class__.__name__
        kwargs=getattr(obj, 'kwargs', {})
        obj.ear=CFMan(obj=obj, **kwargs)
        return obj
