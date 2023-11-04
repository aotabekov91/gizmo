import os

class DirMixin:

    def assignId(self):

        self.m_folder=None
        if os.path.exists(self.m_source):
            f=os.path.dirname(self.m_source)
            self.m_folder=f

    def load(self):

        self.m_data = []
        self.assignId()
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
            for d in self.m_data:
                e=self.element_class(
                        data=d,
                        index=d,
                        model=self)
                self.m_elements[d] = e
                self.elementCreated.emit(e)
            self.loaded.emit()

    def sourceElement(self):

        return self.m_elements.get(
                self.m_source, None)
