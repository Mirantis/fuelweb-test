from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView


class Node(AbstractView):
    def __init__(self, parent=None):
        self.name = HtmlElement(
            xpath=".//div[@class='node-name']", element_name="Cluster name")

        self._select = HtmlElement(
            xpath=".//div[@class='node-select']", element_name="Select tick")

        self.status = HtmlElement(
            xpath=".//div[@class='node-status']", element_name="Status")
        AbstractView.__init__(self, parent)

    def get_name(self):
        return self.name.get_value()

    def get_status(self):
        return self.status.get_value().strip()

    def is_selected(self):
        return self._select.get_element().is_displayed()

    def select(self):
        if self.is_selected():
            return Result("Node is already selected")
        else:
            return self.name.click()
