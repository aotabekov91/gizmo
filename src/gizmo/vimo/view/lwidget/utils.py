from PyQt5.QtWidgets import QListWidgetItem

class ListWidgetItem(QListWidgetItem):

    def setElement(self, e):
        self.m_elem=e
        
    def element(self):
        return self.m_elem
