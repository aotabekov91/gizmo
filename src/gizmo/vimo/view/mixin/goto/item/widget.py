from .view import ViewGo

class WidgetGo(ViewGo):

    def goTo(self, digit=1):

        idx=self.getRowIndex(digit-1)
        self.setCurrentRow(digit-1)
        self.setCurrentIndex(idx)
