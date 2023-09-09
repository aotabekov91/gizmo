from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class InputWidget(QLineEdit):

    def __init__ (self, *args, **kwargs): 

        super().__init__(*args, **kwargs) 

        self.style_sheet='''
            QLineEdit{
                color: black;
                background-color: white;
                border-color: green;
                border-width: 3px;
                border-radius: 15px;
                border-style: outset;
                padding: 0 0 0 10px;
                }
                '''
        
        # self.setStyleSheet(self.style_sheet)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
