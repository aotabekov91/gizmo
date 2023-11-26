from .base import Element

class TableElement(Element):

    m_item=None
    m_litem=None
    m_widget=None

    def setWidget(self, widget):
        self.m_widget=widget

    def widget(self):
        return self.m_widget

    def setItem(self, item):

        self.m_item=item
        item.setElement(self)

    def item(self):
        return self.m_item

    def setListItem(self, item):
        self.m_litem=item

    def listItem(self):
        return self.m_litem
