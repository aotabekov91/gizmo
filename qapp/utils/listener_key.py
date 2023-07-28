from PyQt5 import QtCore
from plugin import KeyListener as BaseListener

class KeyListener(BaseListener, QtCore.QObject): pass
