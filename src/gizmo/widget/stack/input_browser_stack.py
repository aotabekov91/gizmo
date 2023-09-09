from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ..compound import InputBrowser
from .command_stack import CommandStack
from ..base import IconUpDown, ListWidget, InputLabelWidget

class InputBrowserStack(CommandStack):

    def __init__(self, input_class=InputLabelWidget): 

        super(InputBrowserStack, self).__init__()

        main=InputBrowser(input_class)
        super().addWidget(main, 'main', main=True)
