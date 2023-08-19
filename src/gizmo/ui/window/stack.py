from PyQt5 import QtWidgets

from gizmo.widget import StackWidget

from .main import MainWindow

from ..docks import Docks
from ..statusbar import StatusBar

class StackWindow(QtWidgets.QMainWindow):

    def __init__(self, 
            app, 
            display_class=None, 
            view_class=None):

        super().__init__()

        self.app=app
        self.stack=StackWidget()
        self.setCentralWidget(self.stack)
        self.setUI(display_class, view_class)

    def setUI(self, display_class, view_class):

        stl='''
            QWidget {
                color: #101010;
                border-color: #101010;
                background-color: #101010;
                }

            QGraphicsScene {
                border-width: 0px;
                padding: 0 0 0 0;
                }

            QGraphicsView {
                padding: 0 0 0 0;
                border-width: 0px;
                }

            QGraphicsObject{
                border-width: 0px;
                padding: 0 0 0 0;
            }

            QSplitter{
                border-width: 0px;
                padding: 0 0 0 0;
            }

            QLineEdit#statusbarEdit{
                color: white;
                border-width: 0px;
                border-radius: 0px;
                border-color: transparent;
                background-color: transparent;
            }

            QLabel#statusbarColon{
                color: white;
            }

            QLabel#modeLabel {
                color: black;
                background-color: yellow;
            }

            QLabel#pageLabel {
                color: black;
                background-color: yellow ;
            }
               ''' 

        self.main=MainWindow(
                self.app,
                display_class, 
                view_class)

        self.add(self.main, 'main', main=True)

        self.setStyleSheet(stl)
        self.setContentsMargins(0, 0, 0, 0)
        self.stack.setContentsMargins(0, 0, 0, 0)

        main_style_sheet=self.main.styleSheet()

        self.main.setStyleSheet(stl+main_style_sheet)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.main.display.setContentsMargins(0, 0, 0, 0)

        self.docks=Docks(self)
        self.bar=StatusBar(self)
        self.setStatusBar(self.bar)
        self.bar.hide()

    def add(self, *args, **kwargs): 

        self.stack.addWidget(*args, **kwargs)

    def remove(self, *args, **kwargs): 

        self.stack.removeWidget(*args, **kwargs)

    def show(self, *args, **kwargs):

        super().show()
        self.stack.show(*args, **kwargs)
