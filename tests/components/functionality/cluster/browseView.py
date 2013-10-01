from selenium.webdriver.common.by import By
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from engine.poteen.log.resultList import ResultList
from engine.poteen.utils.storage import Storage
from ...generic.abstractView import AbstractView
from ...functionality.cluster.cluster import Cluster
from ....testdata.cluster import TD_Cluster
from ....components.functionality.cluster.actions.view \
    import Cluster_Actions_View
from ....components.functionality.cluster.dialogs.deleteEnvironmentDialog \
    import DeleteEnvironmentDialog
from ....components.functionality.cluster.editView import Cluster_View
from engine.poteen.log.result import Result


class Cluster_BrowseView(AbstractView):
    XPATH_ENVIRONMENTS = "//div[@id='content']//div[@class='cluster-list']" \
                         "//a[contains(@class, 'clusterbox') " \
                         "and div[contains(@class, 'cluster-name')]]"

    def __init__(self, parent=None):
        self.environment = HtmlElement(
            xpath="//div[@id='content']//div[@class='cluster-list']"
                  "//a[contains(@class, 'clusterbox') "
                  "and div[contains(@class, 'cluster-name') "
                  "and text()='{name}']]",
            element_name="Environment {name}"
        )

        self.newEnvironment = Link(
            xpath="//div[@id='content']//div[@class='cluster-list']"
                  "//div[contains(@class, 'clusterbox create-cluster')]",
            element_name="New environment")

        AbstractView.__init__(self, parent)
        self.url = "#clusters"

    def get_clusters(self):
        return [Cluster(x) for x in self.get_action_bot().find_elements(
            By.XPATH, self.XPATH_ENVIRONMENTS)]

    def click_add_new_cluster(self, key="cluster"):
        Storage.put(key, TD_Cluster())
        return self.newEnvironment.click_and_wait()

    def remove(self, name):
        rl = ResultList("Delete environment {name}".format(name=name)) \
            .push(self.environment.find(name=name).click_and_wait()) \
            .push(Cluster_View().click_actions_tab()) \
            .push(Cluster_Actions_View().click_delete_cluster_button()) \
            .push(DeleteEnvironmentDialog().delete())
        env = self.environment.find(name=name)
        if env.is_found():
                WaitBot().wait_for_web_element_disappears(env.get_element())
        return rl

    def remove_all(self):
        rl = ResultList("Remove all existing environments")
        _list = []
        for env in self.get_clusters():
            _list.append(env.get_name())
        rl.info("There is(are) {} environments to remove. Names: {}".format(
            len(_list), str(_list)
        ))
        for name in _list:
            rl.push(self.remove(name))
        rl.info("All environments were removed")
        return rl

    def select(self, name):
        return ResultList("Select environment [{}]".format(name)) \
            .push(self.environment.find(name=name).click_and_wait()
            .push(self.get_wait_bot().wait_for_time(2)))

    def select_by_key(self, key):
        return self.select(Storage.get(key).name)

    def verify_clusters_amount(self, value):
        return Result(
            "Verify if amount of clusters is {value}"
            .format(value=value),
            len(self.get_clusters()) == value
        )
