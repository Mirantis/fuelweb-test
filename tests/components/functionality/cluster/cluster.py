from engine.poteen.elements.basic.htmlElement import HtmlElement
from ...generic.abstractView import AbstractView


class Cluster(AbstractView):
    DEPLOYMENT_MODE_MULTI_NODE = "Multi-node"
    DEPLOYMENT_MODE_MULTI_NODE_WITH_HA = "Multi-node with HA"

    def __init__(self, parent=None):
        self.clusterName = HtmlElement(
            xpath="./div[@class='cluster-name']",
            element_name="Cluster name"
        )
        self.status = HtmlElement(
            xpath="./div[@class='cluster-status']",
            element_name="Status"
        )

        AbstractView.__init__(self, parent)

    def get_name(self):
        return self.clusterName.get_value()

    def get_status(self):
        return self.status.get_value().strip()

    def verify_status(self, status):
        return self.get_status().verify_value(status)
