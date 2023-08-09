from PyQt5 import QtWidgets, QtCore 

class InputWidget(QtWidgets.QWidget):

    def __init__(self, parent):

        super().__init__(parent)

        self.setStyleSheet('''
            QWidget{
                font-size: 16px;
                color: white;
                border-radius: 15px;
                border-style: outset;
                background-color: rgba(0, 0, 0, .8); 
                padding: 15px 15px 15px 15px;
                }
            ''')

        self.setup()

        self.label.hide()
        self.field.hide()

        self.parent().installEventFilter(self)

    def setup(self):

        self.label=QtWidgets.QLabel()
        self.field=QtWidgets.QTextEdit()

        layout=QtWidgets.QVBoxLayout()
        layout.setSpacing(5)

        layout.addWidget(self.label)
        layout.addWidget(self.field)

        self.setLayout(layout)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def updatePosition(self):

        parent_rect = self.parent().rect()

        if parent_rect:

            pwidth=parent_rect.width()
            pheight=parent_rect.height()

            w=int(parent_rect.width()*0.7)
            h=self.height() if self.height()>150 else 150 

            self.setFixedSize(w, h)

            x=int(pwidth/2-self.width()/2)
            # y=int(pheight/2-self.height()/2)
            y=250

            self.setGeometry(x, y, w, h)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.Resize
        if c1:
            if widget==self.parent():
                self.updatePosition()
                event.accept()
                return True
        return False
