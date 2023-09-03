from PyQt5 import QtWidgets, QtCore

from gizmo.widget import StackWidget

from ..docks import Docks
from .main import MainWindow
from ..statusbar import StatusBar

class StackWindow(QtWidgets.QMainWindow):

    windowResized=QtCore.pyqtSignal()

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

            QLineEdit#Statusbar_edit{
                color: white;
                border-width: 0px;
                border-radius: 0px;
                border-color: transparent;
                background-color: transparent;
            }

            QLabel#Powerline_mode {
                color: black;
                padding: 0 5px 0 5px;
                qproperty-alignment: AlignCenter;
                background-color: yellow;
            }

            QLabel#Powerline_keys {
                color: white;
                padding: 0 5px 0 5px;
                qproperty-alignment: AlignCenter;
            }

            QLabel#Powerline_page {
                color: black;
                padding: 0 5px 0 5px;
                qproperty-alignment: AlignCenter;
                background-color: yellow ;
            }

            QLabel#Statusbar_colon{
                color: white;
            }

            QListWidget#ExecMode_List{
                border-width: 0px;
                border-color: transparent;
                background-color: transparent;
            }
            QListWidget#ExecMode_List::item{
                border-width: 0px;
                border-radius: 0px;
            }
            QListWidget#ExecMode_List::item:selected{
                border-width: 0px;
                background-color: gray;
                border-color: transparent;
            }
            QWidget#ExecMode_ListItem{
                color: white;
                border-width: 0px;
                }
               ''' 

        self.main=MainWindow(
                self.app,
                display_class, 
                view_class)

        self.add(self.main, 'main', main=True)

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

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.windowResized.emit()
