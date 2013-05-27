from engine.poteen.elements.basic.htmlElement import HtmlElement
from ...generic.abstractView import AbstractView


class Cluster(AbstractView):
    name = HtmlElement(
        xpath="./div[@class='cluster-name']",
        element_name="Cluster name")

    status = HtmlElement(
        xpath="./div[@class='cluster-status']",
        element_name="Status")

    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)

    def get_name(self):
        return self.name.get_value()

    def get_status(self):
        return self.status.get_value().strip()
