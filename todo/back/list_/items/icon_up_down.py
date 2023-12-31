import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .up_down import UpDown

class IconUpDown (UpDown):

    def getLayout(self):

        layout =super().getLayout()
        self.icon=QLabel()
        up_down_container=QWidget(
                objectName='upDownContainer')
        up_down_container.setLayout(
                layout)
        icon_text_layout = QHBoxLayout()
        icon_text_layout.setSpacing(10)
        icon_text_layout.addWidget(
                self.icon)
        icon_text_layout.addWidget(
                up_down_container)
        icon_text_container=QWidget(
                objectName='iconTextContainer')
        icon_text_container.setLayout(
                icon_text_layout)
        layout=QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(icon_text_container)
        self.icon.hide()
        return layout

    def setIcon(self, imagePath):

        self.icon.path = imagePath
        if os.path.isfile(imagePath):
            scale=self.icon.size()
            w, h=scale.width(), scale.height()
            self.icon.setPixmap(QPixmap(imagePath).scaled(w, h, Qt.KeepAspectRatio))
            self.icon.show()

    def setData(self, data):

        super().setData(data)
        if data:
            if data.get('icon', False): self.setIcon(data['icon'])

    def setFixedWidth(self, width):

        super().setFixedWidth(width)

        substract=40

        if self.icon.isVisible():
            substract+=17 # icon padding
            substract+=self.icon.size().width()
        width-=substract

        self.up.setFixedWidth(width)
        self.down.setFixedWidth(width)
