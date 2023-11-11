class Annotate:

    canAnnotate=True

    def setElement(self, e):

        super().setElement(e)
        if e: self.connectAnnotation(e)

    def connectAnnotation(self, e):

        s=['Added', 'Removed', 'Updated']
        for i in s:
            es=getattr(e, f'annotation{i}', None)
            if es: es.connect(self.reactOnAnnotation)

    def reactOnAnnotation(self, data):

        self.refresh(dropCache=True)
        self.select()

    def annotate(self, data):
        self.m_element.annotate(data)

    def deannotate(self, data):
        self.m_element.deannotate(data)
