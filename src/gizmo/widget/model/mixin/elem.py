class ElementMixin:

    def sourceElement(self):

        for i, e in self.m_elements.items():
            if e.data()==self.m_source:
                return e 

    def load(self):

        if self.element_class:
            e={}
            for i, d in enumerate(self.m_data):
                e[i+1] = self.element_class(
                        data=d,
                        index=i+1,
                        model=self)
            self.m_elements=e
