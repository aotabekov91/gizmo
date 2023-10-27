from PyQt5 import QtCore
from gizmo.ui import View as BaseView

from .item import Item
from .cursor import Cursor
from .layout import Layout

class View(BaseView):

    def __init__(
            self, 
            *args,
            item_class=Item,
            layout_class=Layout,
            cursor_class=Cursor,
            **kwargs,
            ):

        self.m_cache = {}
        super().__init__(
                *args,
                item_class=item_class,
                cursor_class=cursor_class,
                layout_class=layout_class,
                **kwargs
                )

