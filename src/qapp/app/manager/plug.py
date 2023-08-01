import os
import sys
import importlib

from ast import literal_eval

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Plugs(QObject):

    def __init__(self, app):

        super(Plugs, self).__init__(app)

        self.app=app
        self.plugs={}

    def load(self):

        # if self.app.config.has_section('Manager'):
            # self.manager_path=self.app.config.get('Manager', 'plugs_path') 

        self.plugs_path=os.path.join(self.app.path, 'plugs')
        if os.path.exists(self.plugs_path):
            sys.path.append(self.plugs_path)
            for p_name in os.listdir(self.plugs_path):
                if not p_name.startswith('__'):
                    plug_module=importlib.import_module(p_name)
                    if hasattr(plug_module, 'get_plug_class'):
                        self.addPlug(plug_module.get_plug_class())

        self.app.actionRegistered.emit()

    def loadPlug(self, plug_class):

        self.addPlug(plug_class)
        self.app.actionRegistered.emit()

    def addPlug(self, plug_class):

        plug=plug_class(self.app)
        self.plugs[plug.name]=plug
        setattr(self, plug.name, plug)
