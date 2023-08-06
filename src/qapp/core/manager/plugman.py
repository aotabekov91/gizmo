import os
import sys
import importlib

class Plugman:

    def __init__(self, app):

        super(Plugman, self).__init__()

        self.app=app
        self.path=os.path.join(self.app.path, 'plugs')

        self.app.intents=[]
        self.app.entities=[]

        self.plugs={}

    def cleanup(self): pass #TODO

    def install(self): pass #TODO

    def load(self):

        if os.path.exists(self.path):
            sys.path.append(self.path)
            for path in os.listdir(self.path):
                self.read(path, register=False)

            self.app.actionRegistered.emit()

            paths=[self.app.entities, self.app.intents]
            self.app.registerByUmay(paths)

    def read(self, plug_path, register=True):

        plug_module=importlib.import_module(plug_path)
        if hasattr(plug_module, 'get_plug_class'):
            self.initiate(plug_module.get_plug_class())

        if register: self.app.actionRegistered.emit()

    def initiate(self, plug_class):

        # try:

        plug=plug_class(app=self.app)
        self.plugs[plug.name]=plug
        setattr(self, plug.name, plug)

        if plug.intents:
            for i in plug.intents:
                print(i)
                name=i['name']
                i['name']=f"{self.app.name}_{name}"
            self.app.intents+=plug.intents
        if plug.entities:
            for i in plug.intents:
                name=i['intentName']
                i['intentName']=f"{self.app.name}_{name}"
            self.app.entities+=plug.entities

        # except:
        #     print('Could not not plug: ', plug_class.__name__)
