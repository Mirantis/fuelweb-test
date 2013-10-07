from selenium.webdriver.common.by import By

from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result

from ....generic.abstractView import AbstractView
from ....elements.Checkbox import Checkbox


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
            xpath=".//label[@class='node-checkbox']"
                  "//div[@class='custom-tumbler']/input",
            element_name="Checkbox")

        self.status = HtmlElement(
            xpath=".//div[@class='node-status']", element_name="Status")

        self.details = HtmlElement(
            xpath=".//div[@class='node-details']",
            element_name="Node details icon")

        AbstractView.__init__(self, parent)

    def get_name(self):
        return self.name.get_value()

    def get_status(self):
        return self.status.get_value().strip()

    def is_selected(self):
        return self._checkbox.verify_value("on")

    def verify_checkbox(self, expectedValue):
        return self._checkbox.verify_value(expectedValue)

    def set_checkbox(self, value):
        return self._checkbox.set_value(value)

    def select(self):
        if self.is_selected().i_passed():
            return Result("Node is already selected")
        else:
            return self._checkbox.set_value(Checkbox.VALUE_ON)

    def click_node_details(self):
        return self.details.click()

    def get_roles(self):
        roles_elements = ActionBot().find_elements(
            By.XPATH, ".//div[@class='roles']//li")
        return [HtmlElement(element=we).get_value() for we in roles_elements]
