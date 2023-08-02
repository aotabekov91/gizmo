from PyQt5 import QtCore

from ..manager import Manager
from ..window import StackWindow

from ...plug import PlugApp

class BaseApp(PlugApp):

    actionRegistered=QtCore.pyqtSignal()

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.setUI()
        self.initiate()

    def setParser(self):

        super().setParser()
        self.parser.add_argument(
                'file', nargs='?', default=None, type=str)

    def setUI(self):

        self.setManager()
        self.setStack()

    def setStack(self, display_class=None, view_class=None):

        self.stack=StackWindow(self, display_class, view_class)

    def setManager(self, 
                   manager=None, 
                   buffer=None, 
                   plug=None, 
                   mode=None):

        if not manager: manager=Manager
        self.manager=manager(self, buffer, mode, plug)

    def initiate(self):

        self.plugs.load()
        self.modes.load()
        self.parse()
        self.stack.show()

    def parse(self):

        args, unkw = self.parser.parse_known_args()
        self.main.open(filePath=args.file)
