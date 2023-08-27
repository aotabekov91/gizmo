from PyQt5 import QtCore
from .listener_event import EventListener

class SetKeys(type(QtCore.QObject)):

    def __call__(cls, *args, **kwargs):

        obj=type.__call__(cls, *args, **kwargs)
        obj.listener=EventListener(obj=obj)
        obj.name=obj.__class__.__name__
        return obj
