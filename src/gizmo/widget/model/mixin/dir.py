import os

class DirMixin:

    def assignId(self, source):

        self.m_folder=None
        if os.path.exists(source):
            f=os.path.dirname(source)
            self.m_folder=f

    def load(self, source):

        self.m_data = []
        self.setFiles()
        self.setElements()

    def setFiles(self):

        if self.m_folder:
            for f in os.listdir(self.m_folder):
                c=self.isCompatible(f)
                if not c: continue
                p = os.path.join(
                        self.m_folder, f)
                self.m_data.append(p)

    def setElements(self):

        if self.element_class:
            c= self.element_class
            for d in self.m_data:
                self.m_elements[d] = c(
                        data=d,
                        index=d,
                        model=self)

    def sourceElement(self):

        return self.m_elements.get(
                self.m_source, None)
