from engine.poteen.elements.basic.link import Link
from ..generic.abstractView import AbstractView


class Main(AbstractView):
    def __init__(self, parent=None):
        self.environments = Link(
            xpath="//a[text()='Environments']",
            element_name="Environments"
        )

        self.releases = Link(
            xpath="//a[text()='Releases']",
            element_name="Releases"
        )

        self.support = Link(
            xpath="//a[text()='Support']",
            element_name="Support"
        )

        AbstractView.__init__(self, parent)
        self.url = ""
