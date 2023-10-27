from PyQt5.QtCore import QObject

class Cursor(QObject):

    def __init__(self, view): 

        super().__init__(view)
        view.itemMouseMoveOccured.connect(
                self.on_mouseMove)
        view.itemMousePressOccured.connect(
                self.on_mousePress)
        view.itemMouseReleaseOccured.connect(
                self.on_mouseRelease)
        view.itemMouseDoubleClickOccured.connect(
                self.on_doubleClick)
        self.setup()

    def setup(self):
        pass

    def on_mouseMove(self, view, item, event): 
        pass

    def on_mouseRelease(self, view, item, event): 
        pass

    def on_mousePress(self, view, item, event):
        pass

    def on_doubleClick(self, view, item, event):
        pass
