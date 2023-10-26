from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):

    resized=QtCore.pyqtSignal()
    
    def __init__(
            self, *args, **kwargs):

        super().__init__(
                *args, **kwargs)
        self.setUI()

    def setUI(self):

        self.container=QtWidgets.QWidget(
                objectName='MainWindowContainer'
                )
        self.m_layout=QtWidgets.QVBoxLayout()
        self.m_layout.setContentsMargins(
                0,0,0,0)
        self.m_layout.setSpacing(0)
        self.container.setLayout(
                self.m_layout)
        self.setCentralWidget(self.container)

        self.setAcceptDrops(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.resized.emit()
