import os
import sys
import importlib

from PyQt5 import QtCore

class Plugman(QtCore.QObject):

    def __init__(self, app):

        super(Plugman, self).__init__(app)

        self.app=app
        self.plugs={}

    def load(self):

        self.plugs_path=os.path.join(self.app.path, 'plugs')

        if os.path.exists(self.plugs_path):
            sys.path.append(self.plugs_path)
            for p_name in os.listdir(self.plugs_path):
                if not p_name.startswith('__'):
                    plug_module=importlib.import_module(p_name)
                    if hasattr(plug_module, 'get_plug_class'):
                        self.addPlug(plug_module.get_plug_class())

        self.app.actionRegistered.emit()

    def addPlug(self, plug_class, action_register=False):

        # try:

        plug=plug_class(app=self.app)
        self.plugs[plug.name]=plug
        setattr(self, plug.name, plug)
        if action_register: self.app.actionRegistered.emit()

        # except:
        #     print('Could not not plug: ', plug_class.__name__)
