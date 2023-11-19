from gizmo.widget import ListWidget, StackedWidget

class CommandWindow(StackedWidget):

    def __init__(
            self, 
            app, 
            *args, 
            **kwargs):

        self.activated=False
        super(CommandWindow, self).__init__(
                *args, **kwargs)

        self.app=app
        self.setUI()

    def setUI(self):

        self.app.window.add(
                self, 'command')
        self.addWidget(
                ListWidget(
                    exact_match=True, 
                    check_fields=['down']), 
                'mode')
