from gizmo.widget import ListWidget, CommandStack

class CommandWindow(CommandStack):

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

    # def activate(self): 
    #     self.activated=True
    #     self.app.window.show(
    #             self)
    #     # self.setFixedSize(
    #     #         self.app.window.size())

    # def deactivate(self): 
    #     self.activated=False
    #     self.app.window.show(
    #             self.app.window.main)
