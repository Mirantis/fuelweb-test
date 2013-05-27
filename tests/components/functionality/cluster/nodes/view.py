from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from engine.poteen.log.resultList import ResultList
from ....generic.abstractView import AbstractView
from .listView import Cluster_Nodes_ListView
from tests.components.functionality.cluster.dialogs.environmentDeploymentModeDialog import EnvironmentDeploymentModeDialog


class Cluster_Nodes_View(AbstractView):
    addCompute = Link(
        xpath="//div[@id='tab-nodes']"
              "//div[contains(@class, 'node-list-compute')]"
              "//a[contains(@class, 'btn-add-nodes')]",
        element_name="Add compute")

    addController = Link(
        xpath="//div[@id='tab-nodes']"
              "//div[contains(@class, 'node-list-controller')]"
              "//a[contains(@class, 'btn-add-nodes')]",
        element_name="Add controller")

    computes = Button(
        xpath="//div[@id='tab-nodes']"
              "//div[contains(@class, 'node-list-compute')]",
        element_name="computes")

    controllers = HtmlElement(
        xpath="//div[@id='tab-nodes']"
              "//div[contains(@class, 'node-list-controller')]",
        element_name="controllers")

    deploymentMode = Link(
        xpath="//li[contains(@class, 'change-cluster-mode-btn')]",
        element_name="Deployment mode")

    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)

    def click_add_compute(self):
        return self.addCompute.click()

    def click_add_controller(self):
        return self.addController.click()

    def click_deployment_mode(self):
        return self.deploymentMode.click()

    def select_environment_mode(self, deploymentMode, deploymentType):
        rl = ResultList(
            "Select environment mode [{mode}] type [{type}]".format(
                mode=deploymentMode, type=deploymentType)
        )
        rl.push(self.click_deployment_mode())
        rl.push(EnvironmentDeploymentModeDialog().populate(
            deploymentMode=deploymentMode,
            deploymentType=deploymentType,
            submit=True
        ))


def verify_compute_nodes(self, *args):
    return Cluster_Nodes_ListView(
        self.computes.get_element()
    ).verify_nodes(*args)


def verify_controller_nodes(self, *args):
    return Cluster_Nodes_ListView(
        self.controllers.get_element()
    ).verify_nodes(*args)