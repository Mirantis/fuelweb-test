from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from engine.poteen.log.resultList import ResultList
from ....generic.abstractView import AbstractView
from .....components.functionality.cluster.generic.node import Node
from selenium.webdriver.common.by import By


class Cluster_Nodes_ListView(AbstractView):

    xpath_nodes_by_status = ("//div[contains(@class, 'nodebox') and "
                             "contains(./div/div[@class='node-status']/div, "
                             "'{status}')]")

    def __init__(self, parent=None):
        self.node = HtmlElement(
            xpath=".//div[contains(@class, 'nodebox') and "
                  "not(contains(@class, 'nodebox-gradient')) and "
                  ".//div[@class='node-name' and ./div/text()='{name}']]",
            element_name="Node [{name}]"
        )
        AbstractView.__init__(self, parent)

    def _get_nodes(self, xpath):
        nodes = []
        elements = ActionBot().find_elements(By.XPATH, xpath)
        for i, element in enumerate(elements):
            nodes.append(Node(element))
        return nodes

    def _get_nodes_names(self, xpath):
        nodes = self._get_nodes(xpath)
        nodes_names = []
        for i, n in enumerate(nodes):
            nodes_names.append(n.get_name())
        return nodes_names

    def get_nodes(self):
        return self._get_nodes(".//div[contains(@class, 'nodebox')]")

    def get_nodes_by_status(self, status):
        return self._get_nodes(
            Cluster_Nodes_ListView.xpath_nodes_by_status.format(status=status))

    def get_nodes_names_by_status(self, status):
        return self._get_nodes_names(
            Cluster_Nodes_ListView.xpath_nodes_by_status.format(status=status))

    def select_nodes(self, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(self.node.find(name=name).get_element())
            rl.push(node.select())
        rl.push(self.apply())
        WaitBot().wait_for_disappears(By.XPATH, "//div[contains(@class,'nodes-screen')]")
        WaitBot().wait_for_displays(By.XPATH, "//div[@class='nodes-by-roles-screen']")
        return rl

    def click_nodes(self, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(self.node.find(name=name).get_element())
            rl.push(node.select())
        return rl

    def verify_nodes(self, *args):
        rl = ResultList("Verify nodes")
        for name in args:
            rl.push(Result(
                "Node [{name}] exists".format(name=name),
                self.node.find(name=name).is_found()
            ))
        return rl

    def verify_nodes_not_exist(self, *args):
        rl = ResultList("Verify nodes not exist")
        for name in args:
            rl.push(Result(
                "Node [{name}] not exists".format(name=name),
                self.node.find(name=name).is_not_found()
            ))
        return rl
