from os.path import abspath
from PyQt5.QtWidgets import QFileSystemModel

from .base import Model

class FileSystemModel(
        Model, 
        QFileSystemModel):

    kind='files'
    root_path='/'

    def id(self):
        return '/'

    def setup(self):
        
        super().setup()
        self.setRootPath(self.root_path)

    def getPathIndex(self, path=None):

        path = path or abspath('.')
        return self.index(path)

    def element(self, idx):

        idx=idx or self.currentIndex()
        return self.filePath(idx)
