from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from .abstractView import AbstractView


class AbstractMenu(AbstractView):
    def __init__(self, parent=None):
        self.logo = Link(
            xpath=".//div[@class='navigation-bar']//li[@class='product-logo']",
            element_name="Logo"
        )
        self.nodesTotal = HtmlElement(
            xpath=".//div[@class='navigation-bar']//div[@class='statistic']"
                  "/div[@class='stat-count'][1]",
            element_name="Nodes total"
        )
        self.nodesUnallocated = HtmlElement(
            xpath=".//div[@class='navigation-bar']//div[@class='statistic']"
                  "/div[@class='stat-count'][1]",
            element_name="Nodes unallocated"
        )
        self.notificationsLink = Link(
            xpath=".//div[@class='navigation-bar']"
                  "//li[contains(@class, 'notifications')]",
            element_name="Notifications"
        )
        self.openStackEnvironmentsLink = Link(
            xpath=".//div[@class='navigation-bar']"
                  "//li[contains(.,'OpenStack Environments')]",
            element_name="OpenStack Environments"
        )
        self.supportLink = Link(
            xpath=".//div[@class='navigation-bar']"
                  "//li[contains(.,'OpenStack Support')]",
            element_name="OpenStack Support"
        )

        AbstractView.__init__(self, parent)

    