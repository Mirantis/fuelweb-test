from engine.poteen.elements.basic.HtmlElement import HtmlElement
from engine.poteen.elements.basic.Link import Link
from .AbstractView import AbstractView


class AbstractMenu(AbstractView):
    logo = Link(
        xpath=".//div[@class='navigation-bar']//li[@class='product-logo']",
        element_name="Logo")

    nodesTotal = HtmlElement(
        xpath=".//div[@class='navigation-bar']//div[@class='statistic']"
              "/div[@class='stat-count'][1]",
        element_name="Nodes total")

    nodesUnallocated = HtmlElement(
        xpath=".//div[@class='navigation-bar']//div[@class='statistic']"
              "/div[@class='stat-count'][1]",
        element_name="Nodes unallocated")

    notificationsLink = Link(
        xpath=".//div[@class='navigation-bar']"
              "//li[contains(@class, 'notifications')]",
        element_name="Notifications")

    openStackEnvironmentsLink = Link(
        xpath=".//div[@class='navigation-bar']"
              "//li[contains(.,'OpenStack Environments')]",
        element_name="OpenStack Environments")

    supportLink = Link(
        xpath=".//div[@class='navigation-bar']"
              "//li[contains(.,'OpenStack Support')]",
        element_name="OpenStack Support")

    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)

    