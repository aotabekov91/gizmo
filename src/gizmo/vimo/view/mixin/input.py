class Input:

    canInput=True

    def inputGetWidgets(self):

        widgets=[]
        for i in range(self.count()):
            item=self.item(i)
            e=item.element()
            w=e.widget()
            if hasattr(w, 'hasWidgets'):
                for i in w.widgets().values():
                    if hasattr(i, 'canEdit'):
                        widgets+=[i]
        return widgets
