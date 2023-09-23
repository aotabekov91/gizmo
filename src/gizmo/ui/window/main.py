from PyQt5 import QtWidgets, QtCore

from ..display import Display

class MainWindow(QtWidgets.QMainWindow):

    resized=QtCore.pyqtSignal()
    viewCreated=QtCore.pyqtSignal(object)
    
    def __init__(self, 
                 app, 
                 display_class=None, 
                 view_class=None):

        super().__init__()

        self.app=app
        self.name=self.__class__.__name__
        self.s_settings=app.config.get(
                self.name, {})

        self.setUI(display_class, view_class)

    def setDisplay(self, display_class, view_class=None):

        self.main_widget=QtWidgets.QWidget()

        self.main_layout=QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)
        if not display_class: 
            display_class=Display
        self.display=display_class(self.app, self, view_class)
        self.display.viewCreated.connect(self.viewCreated)
        self.main_layout.addWidget(self.display)
        self.setCentralWidget(self.main_widget)

    def setUI(self, display_class, view_class):

        self.setDisplay(display_class, view_class)
        self.setAcceptDrops(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def close(self): 
        self.app.exit()

    def open(self, filePath, how='reset', focus=True): 

        data=self.app.buffer.load(filePath)
        self.display.open(data, how, focus)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.resized.emit()
