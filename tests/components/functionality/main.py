from ..generic.AbstractView import AbstractView


class Main(AbstractView):
    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)
        self.url = ""
