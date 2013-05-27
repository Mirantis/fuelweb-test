from selenium.webdriver.common.by import By
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from ...generic.abstractView import AbstractView
from ...functionality.cluster.cluster import Cluster


class BrowseView(AbstractView):
    XPATH_ENVIRONMENTS = "//div[@id='content']//div[@class='cluster-list']" \
                         "//a[contains(@class, 'clusterbox') " \
                         "and div[contains(@class, 'cluster-name')]]"

    environment = HtmlElement(
        xpath="//div[@id='content']//div[@class='cluster-list']"
              "//a[contains(@class, 'clusterbox') "
              "and div[contains(@class, 'cluster-name') and text()='{name}']]",
        element_name="Environment {name}")

    newEnvironment = Link(
        xpath="//div[@id='content']//div[@class='cluster-list']"
              "//div[contains(@class, 'clusterbox create-cluster')]",
        element_name="New environment")

    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)
        self.url = "#clusters"

    def get_clusters(self):
        return [Cluster(x) for x in self.get_action_bot().find_elements(
            By.XPATH, self.XPATH_ENVIRONMENTS)]

    def click_add_new_environment(self):
        pass
