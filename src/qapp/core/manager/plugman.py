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
            for n in os.listdir(self.plugs_path):
                if not n.startswith('__'):
                    pmod=importlib.import_module(n)
                    if hasattr(pmod, 'get_plug_class'):
                        self.addPlug(pmod.get_plug_class())

        self.app.actionRegistered.emit()

    def addPlug(self, plug_class, action_register=False):

        # try:

        plug=plug_class(app=self.app)
        self.plugs[plug.name]=plug
        setattr(self, plug.name, plug)
        if action_register: self.app.actionRegistered.emit()

        # except:
        #     print('Could not not plug: ', plug_class.__name__)
