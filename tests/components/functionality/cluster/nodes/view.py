from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from engine.poteen.log.resultList import ResultList
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from .listView import Cluster_Nodes_ListView
from ..dialogs.environmentDeploymentModeDialog \
    import EnvironmentDeploymentModeDialog


class Cluster_Nodes_View(AbstractView):
    def __init__(self, parent=None):
        self.addCompute = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-compute')]"
                  "//a[contains(@class, 'btn-add-nodes')]",
            element_name="Add compute"
        )
        self.addController = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-controller')]"
                  "//a[contains(@class, 'btn-add-nodes')]",
            element_name="Add controller"
        )
        self.addCinder = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-cinder')]"
                  "//a[contains(@class, 'btn-add-nodes')]",
            element_name="Add controller"
        )
        self.computes = Button(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-compute')]",
            element_name="computes"
        )
        self.controllers = HtmlElement(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-controller')]",
            element_name="controllers"
        )
        self.cinders = Button(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-cinder')]",
            element_name="cinders"
        )
        self.deploymentMode = Link(
            xpath="//li[contains(@class, 'change-cluster-mode-btn')]",
            element_name="Deployment mode"
        )
        self.alertError = HtmlElement(
            xpath="//div[contains(@class, 'alert-block') "
                  "and contains(@class, 'global-error')]/p",
            element_name="Alert Error"
        )

        AbstractView.__init__(self, parent)

    def click_add_compute(self):
        return self.addCompute.click_and_wait()

    def click_add_controller(self):
        return self.addController.click_and_wait()

    def click_add_cinder(self):
        return self.addCinder.click_and_wait()

    def click_deployment_mode(self):
        return self.deploymentMode.click()

    def select_environment_mode(self, deploymentMode):
        rl = ResultList(
            "Select environment mode [{mode}]".format(
                mode=deploymentMode)
        )
        rl.push(self.click_deployment_mode())
        rl.push(EnvironmentDeploymentModeDialog().populate(
            deploymentMode=deploymentMode,
            submit=True
        ))
        return rl

    def verify_cinder_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.cinders.get_element()
        ).verify_nodes(*args)

    def verify_compute_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.computes.get_element()
        ).verify_nodes(*args)

    def verify_controller_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.controllers.get_element()
        ).verify_nodes(*args)

    def get_nodes_controllers(self):
        return Cluster_Nodes_ListView(self.controllers.get_element())\
            .get_nodes()

    def get_nodes_computes(self):
        return Cluster_Nodes_ListView(self.computes.get_element())\
            .get_nodes()

    def get_nodes_cinders(self):
        return Cluster_Nodes_ListView(self.cinders.get_element())\
            .get_nodes()

    def verify_controller_nodes_not_exist(self, *args):
        return Cluster_Nodes_ListView(
            self.computes.get_element()
        ).verify_nodes_not_exist(*args)

    def verify_error_contains(self, *args):
        rl = ResultList("Verify error alert contains")
        for string in args:
            rl.push(Result(
                "String [{string}] exists".format(string=string),
                self.alertError.get_value().find(string) != -1
            ))
        return rl
