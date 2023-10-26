import os
from PyQt5 import QtGui, QtCore, QtWidgets

from .base import ItemWidget

class Icon(ItemWidget):

    def setUI(self):

        style_sheet = '''
            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                color: transparent;
                background-color: transparent;
                }
            QLabel{
                padding: 0 0 0 0;
                background-color: transparent;
                }
                '''
        self.icon = QtWidgets.QLabel()
        w=QtWidgets.QWidget()
        layout= QtWidgets.QHBoxLayout()
        layout.setContentsMargins(
                20,20,20,20)
        layout.addStretch()
        layout.addWidget(
                self.icon, 
                QtCore.Qt.AlignCenter)
        layout.addStretch()
        w.setLayout(layout)
        layout=QtWidgets.QHBoxLayout()
        layout.setContentsMargins(
                20,20,20,20)
        layout.addStretch()
        layout.addWidget(
                w, 
                QtCore.Qt.AlignCenter)
        layout.addStretch()
        return layout, style_sheet

    def setIcon(self, path):

        self.icon.path = path
        if os.path.isfile(path):
            s=self.icon.size()
            pmap=QtGui.QPixmap(path)
            pmap=pmap.scaled(
                    s.width(), 
                    s.height(),
                    QtCore.Qt.KeepAspectRatio)
            self.icon.setPixmap(pmap)
            self.icon.show()

    def setData(self, data):

        if data.get('icon', False): 
            self.setIcon(data['icon'])
