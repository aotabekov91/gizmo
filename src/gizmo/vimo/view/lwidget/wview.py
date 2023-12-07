from PyQt5 import QtCore
from gizmo.vimo.view import mixin
from gizmo.widget import ListWidget
from gizmo.widget import TableWidget

from ..base import View
from .utils import ListWidgetItem

class WListWidgetView(
        mixin.Input,
        mixin.WidgetGo,
        View,
        ListWidget,
        ):

    widget_map={}
    widget_class=TableWidget
    list_item_class=ListWidgetItem
    widgetDataChanged=QtCore.pyqtSignal(object)

    def setModel(self, model=None, **kwargs):

        if id(self.m_model)==id(model): 
            return
        self.clear()
        super().setModel(model)
        for i in range(model.rowCount()):
            r=model.index(i, 0)
            e=model.itemFromIndex(r).element()
            self.addElement(e)
        self.reconnectModel()


    def reconnectModel(self, kind='connect'):

        m=self.m_model
        if not m: return
        if kind=='connect':
            m.elementAdded.connect(
                    self.addElement)
            m.elementRemoved.connect(
                    self.removeElement)
        else:
            m.elementAdded.disconnect(
                    self.addElement)
            m.elementRemoved.disconnect(
                    self.removeElement)

    def addElement(self, e):

        m=e.model()
        i=self.list_item_class()
        i.setElement(e)
        w=self.widget_class(
                item=i,
                view=self,
                element=e,
                wmap=self.widget_map)
        w.widgetDataChanged.connect(
                m.updateTableRow)
        self.addItem(i)
        self.setItemWidget(i, w) 
        self.resized.connect(w.adjustSizeHint)
        self.resized.emit(self)

    def removeElement(self, e):

        for i in range(self.count()):
            item=self.item(i)
            if item.element()==e:
                return self.takeItem(i)

    def clear(self):

        self.reconnectModel('disconnect')
        super().clear()
