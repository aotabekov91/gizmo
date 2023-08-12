from PyQt5 import QtWidgets

from .main import MainWindow
from ..display import Display
from ....widget import StackWidget

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
                border-color: red;
                background-color: green;
                }

            QGraphicsView {
                padding: 0 0 0 0;
                border-width: 0px;
                color: white;
                border-color: white;
                background-color: white;
                }
            QGraphicsObject{
                border-width: 0px;
                padding: 0 0 0 0;
                background-color: purple;
            }
            QSplitter{
                border-width: 0px;
                padding: 0 0 0 0;
                background-color: purple;
            }

               ''' 

        self.app.main=MainWindow(
                self.app,
                display_class, 
                view_class)
        self.add(self.app.main, 'main', main=True)

        self.setStyleSheet(stl)
        self.setContentsMargins(0, 0, 0, 0)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.app.main.setContentsMargins(0, 0, 0, 0)
        self.app.main.display.setContentsMargins(0, 0, 0, 0)

    def add(self, *args, **kwargs): 

        self.stack.addWidget(*args, **kwargs)

    def remove(self, *args, **kwargs): 

        self.stack.removeWidget(*args, **kwargs)

    def show(self, *args, **kwargs):

        super().show()
        self.stack.show(*args, **kwargs)
