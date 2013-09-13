
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from tests.components.elements.Checkbox import Checkbox


class Node(AbstractView):
    def __init__(self, parent=None):
        self.name = HtmlElement(
            xpath=".//div[@class='node-name']//p[@class='node-renameable']",
            element_name="Cluster name"
        )

        self.role = HtmlElement(
            xpath=".//div[@class='roles']//li",
            element_name="Cluster role"
        )

        self._checkbox = Checkbox(
            xpath=".//div[@class='node-checkbox']"
                  "//div[@class='custom-tumbler']/input",
            element_name="Checkbox")

        self.status = HtmlElement(
            xpath=".//div[@class='node-status']", element_name="Status")

        self.hardware = HtmlElement(
            xpath=".//div[@class='node-hardware']", element_name="Hardware")

        AbstractView.__init__(self, parent)

    def get_name(self):
        return self.name.get_value()

    def get_status(self):
        return self.status.get_value().strip()

    def verify_checkbox(self, expectedValue):
        return self._checkbox.verify_value(expectedValue)

    def set_checkbox(self, value):
        return self._checkbox.set_value(value)

    def select(self):
        if self.verify_checkbox("on").i_passed():
            return Result("Node is already selected")
        else:
            return self.set_checkbox("on")

    def click_hardware(self):
        return self.hardware.click()
