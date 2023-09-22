from PyQt5 import QtCore
from .listener_event import EventListener

class MetaKey(type(QtCore.QObject)):

    def __call__(cls, *args, **kwargs):

        obj=type.__call__(cls, *args, **kwargs)
        obj.name=obj.__class__.__name__
        obj.listener=EventListener(obj=obj)
        return obj
