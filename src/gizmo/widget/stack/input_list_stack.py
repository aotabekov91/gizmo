from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ..compound import InputList
from .command_stack import CommandStack
from ..base import IconUpDown, ListWidget, InputLabelWidget

class InputListStack(CommandStack):

    def __init__(self, 
                 list_class=ListWidget, 
                 input_class=InputLabelWidget, 
                 **kwargs): 

        super(InputListStack, self).__init__()

        main=InputList(list_class, input_class, **kwargs)
        super().addWidget(main, 'main', main=True)
