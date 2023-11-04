
class ElementMixin:

    def sourceElement(self):

        for i, e in self.m_elements.items():
            if e.data()==self.m_source:
                return e 

    def load(self):

        if self.element_class:
            elems={}
            for i, d in enumerate(self.m_data):
                e = self.element_class(
                        data=d,
                        index=i+1,
                        model=self)
                elems[i+1] = e 
                self.elementCreated.emit(e)
            self.m_elements=elems
            self.loaded.emit()
