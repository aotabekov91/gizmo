from PyQt5.QtGui import QStandardItem

class StandardItem(QStandardItem):

    def setElement(self, elem):
        self.m_elem=elem

    def element(self):
        return self.m_elem

