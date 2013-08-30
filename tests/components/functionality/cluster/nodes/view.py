from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.decorators import catch_stale_error
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from engine.poteen.error import ElementNotFoundException
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
        self.addComputeDisabled = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-compute')]"
                  "//*[contains(@class, 'disabled') and  contains(.,'Add')]",
            element_name="Add compute disabled"
        )
        self.addControllerDisabled = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-controller')]"
                  "//*[contains(@class, 'disabled') and  contains(.,'Add')]",
            element_name="Add controller disabled"
        )
        self.addCinderDisabled = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-cinder')]"
                  "//*[contains(@class, 'disabled') and  contains(.,'Add')]",
            element_name="Add controller disabled"
        )
        self.deleteCompute = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-compute')]"
                  "//a[contains(@class, 'btn-delete-nodes')]",
            element_name="Delete compute"
        )
        self.deleteController = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-controller')]"
                  "//a[contains(@class, 'btn-delete-nodes')]",
            element_name="Delete controller"
        )
        self.deleteCinder = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-cinder')]"
                  "//a[contains(@class, 'btn-delete-nodes')]",
            element_name="Delete cinder"
        )
        self.deleteComputeDisabled = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-compute')]"
                  "//*[contains(@class, 'disabled') "
                  "and  contains(.,'Delete')]",
            element_name="Delete controller disabled"
        )
        self.deleteControllerDisabled = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-controller')]"
                  "//*[contains(@class, 'disabled') "
                  "and  contains(.,'Delete')]",
            element_name="Delete controller disabled"
        )
        self.deleteCinderDisabled = Link(
            xpath="//div[@id='tab-nodes']"
                  "//div[contains(@class, 'node-list-cinder')]"
                  "//*[contains(@class, 'disabled') "
                  "and  contains(.,'Delete')]",
            element_name="Delete controller disabled"
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
        self.controller_placeholder = HtmlElement(
            xpath="//div[contains(@class, 'node-list node-list-controller')]"
                  "//div[contains(@class, 'nodebox nodeplaceholder')]",
            element_name="controller placeholder"
        )
        self.controller_nodelist = HtmlElement(
            xpath="//div[@class= 'node-list node-list-controller']",
            element_name="controller nodelist"
        )
        self.compute_nodelist = HtmlElement(
            xpath="//div[@class= 'node-list node-list-compute']",
            element_name="compute nodelist"
        )
        self.cinder_nodelist = HtmlElement(
            xpath="//div[@class= 'node-list node-list-cinder']",
            element_name="cinder nodelist"
        )
        self.environment_deployment_mode_dialog = HtmlElement(
            xpath="//div[contains(@class, 'modal fade in')]",
            element_name="deployment mode dialog"
        )

        AbstractView.__init__(self, parent)

    def click_add_compute(self):
        return self.addCompute.click_and_wait()

    def click_add_controller(self):
        return self.addController.click_and_wait()

    def click_add_cinder(self):
        return self.addCinder.click_and_wait()

    def click_delete_compute(self):
        return self.deleteCompute.click_and_wait()

    def click_delete_controller(self):
        return self.deleteController.click_and_wait()

    def click_delete_cinder(self):
        return self.deleteCinder.click_and_wait()

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

    @catch_stale_error
    def verify_cinder_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.cinders.get_element()
        ).verify_nodes(*args)

    @catch_stale_error
    def verify_compute_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.computes.get_element()
        ).verify_nodes(*args)

    @catch_stale_error
    def verify_controller_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.controllers.get_element()
        ).verify_nodes(*args)

    def get_nodes_controllers(self):
        return Cluster_Nodes_ListView(self.controllers.get_element()) \
            .get_nodes()

    def get_nodes_computes(self):
        return Cluster_Nodes_ListView(self.computes.get_element()) \
            .get_nodes()

    def get_nodes_cinders(self):
        return Cluster_Nodes_ListView(self.cinders.get_element()) \
            .get_nodes()

    def get_controllers_placeholders(self):
        return Cluster_Nodes_ListView(self.controller_placeholder).get_nodes()

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

    def verify_nodelists_visibility(self, value):
        rl = ResultList("Verify there are 3 node lists")
        rl.push(VerifyBot().verify_visibility(
            self.controller_nodelist.get_element(), value,
            "Controller nodelist"))
        rl.push(VerifyBot().verify_visibility(
            self.compute_nodelist.get_element(), value, "Compute nodelist"))
        rl.push(VerifyBot().verify_visibility(
            self.cinder_nodelist.get_element(), value, "Cinder nodelist"))
        return rl

    def verify_amount(self, elements_names, value):
        elements = None
        result = None
        try:
            if elements_names == "placeholders for controllers":
                elements = self.get_controllers_placeholders()
            elif elements_names == "controllers":
                elements = self.get_nodes_controllers()
            elif elements_names == "computes":
                elements = self.get_nodes_computes()
            elif elements_names == "cinders":
                elements = self.get_nodes_cinders()

            if value == 0:
                result = Result(
                    "Verify if amount of {name} is 0".format(
                        name=elements_names, value=value),
                    VerifyBot().verify_visibility(
                        elements, False, elements_names).i_passed())
            else:
                result = Result(
                    "Verify if amount of {name} is {value}".format(
                        name=elements_names, value=value),
                    len(elements) == value)

        except ElementNotFoundException:
            if value == 0:
                result = Result("There are no {name}".format(
                    name=elements_names), True)
        return result

    def verify_controllers_placeholders_amount(self, value):
        return self.verify_amount("placeholders for controllers", value)

    def verify_controllers_amount(self, value):
        return self.verify_amount("controllers", value)

    def verify_computes_amount(self, value):
        return self.verify_amount("computes", value)

    def verify_cinders_amount(self, value):
        return self.verify_amount("cinders", value)
