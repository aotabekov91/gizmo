from os.path import abspath
from PyQt5.QtWidgets import QFileSystemModel

from .base import Model

class FileSystemModel(
        Model, 
        QFileSystemModel):

    root_path='/'

    def id(self):
        return self.rootPath()

    def setup(self):
        
        super().setup()
        self.setRootPath(self.root_path)

    def getPathIndex(self, path=None):

        path = path or abspath('.')
        return self.index(path)

    def element(self, idx):
        return self.filePath(idx)
