from engine.poteen.elements.basic.htmlElement import HtmlElement
from ...generic.abstractView import AbstractView


class Cluster(AbstractView):
    DEPLOYMENT_MODE_MULTI_NODE = "Multi-node"
    DEPLOYMENT_MODE_MULTI_NODE_WITH_HA = "Multi-node with HA"
    DEPLOYMENT_TYPE_COMPUTE_ONLY = "Compute only"
    DEPLOYMENT_TYPE_COMPUTE_WITH_CINDER = "Compute with Cinder"

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
