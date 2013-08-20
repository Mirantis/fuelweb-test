from ...generic.abstractView import AbstractView


class Releases_Main(AbstractView):
    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)
        self.url = "#releases"
