from PyQt5 import QtWidgets

class ListWidgetItem(QtWidgets.QListWidgetItem):

    def element(self):
        return self.m_element

    def setElement(self, e):
        self.m_element=e

    def widget(self):
        return self.m_element.widget()
