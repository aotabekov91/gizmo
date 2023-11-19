class Go:

    canGo=True

    def go(self, kind, *args, **kwargs):

        if type(kind)==int:
            self.goto(kind)
        elif kind=='first':
            if hasattr(self, 'gotoFirst'):
                self.gotoFirst()
        elif kind=='last':
            if hasattr(self, 'gotoLast'):
                self.gotoLast()
