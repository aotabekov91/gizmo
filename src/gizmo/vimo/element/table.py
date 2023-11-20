from .base import Element

class TableElement(Element):

    def setWidget(self, widget):
        self.m_widget=widget

    def widget(self):
        return self.m_widget

    def setListItem(self, item):
        self.m_item=item

    def listItem(self):
        return self.m_item
