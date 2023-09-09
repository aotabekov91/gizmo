from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class InputWidget (QLineEdit):

    def __init__ (self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 

        self.style_sheet='''
            QLineEdit{
                color: black;
                background-color: white;
                border-color: transparent;
                border-width: 0px;
                border-radius: 10px;
                padding: 0 10px 0 10px;
                border-style: outset;
                }
                '''

        self.setStyleSheet(self.style_sheet)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
