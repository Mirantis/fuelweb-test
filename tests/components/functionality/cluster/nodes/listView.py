from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from engine.poteen.log.resultList import ResultList
from ....generic.abstractView import AbstractView
from tests.components.functionality.cluster.generic.node import Node


class Cluster_Nodes_ListView(AbstractView):
    def __init__(self, parent=None):
        self.node = HtmlElement(
            xpath=".//div[contains(@class, 'nodebox') and "
                  "not(contains(@class, 'nodebox-gradient')) and "
                  ".//div[@class='node-name' and ./div/text()='{name}']]",
            element_name="Node [{name}]"
        )
        AbstractView.__init__(self, parent)

    def select_nodes(self, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(self.node.find(name=name).get_element())
            rl.push(node.select())
        rl.push(self.apply())
        return rl

    def verify_nodes(self, *args):
        rl = ResultList("Verify nodes")
        for name in args:
            rl.push(Result(
                "Node [{name}] exists".format(name=name),
                self.node.find(name=name).is_found()
            ))
        return rl
