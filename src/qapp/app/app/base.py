import os
import inspect
import argparse
import configparser

from PyQt5 import QtCore

from ..manager import Manager
from ..window import StackWindow

from ...plug import PlugApp

class BaseApp(PlugApp):

    actionRegistered=QtCore.pyqtSignal()

    def __init__(self, argv=[], **kwargs):

        super().__init__(argv=[], **kwargs)

        self.setConfig()
        self.setParser()
        self.setUI()
        self.initiate()

    def setParser(self):

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
                'file', nargs='?', default=None, type=str)

    def setConfig(self):

        file_path=os.path.abspath(
                inspect.getfile(self.__class__))
        self.path=os.path.dirname(
                file_path).replace('\\', '/')
        self.configPath=f'{self.path}/config.ini'
        self.config=configparser.RawConfigParser()
        self.config.optionxform=str
        self.config.read(self.configPath)

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

        self.loadPlugs()
        self.loadModes()
        self.parse()

        self.stack.show()

    def loadPlugs(self): self.plugs.load()

    def loadModes(self): self.modes.load()

    def parse(self):

        args, unkw = self.parser.parse_known_args()
        self.main.open(filePath=args.file)
