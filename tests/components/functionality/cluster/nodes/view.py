from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.decorators import catch_stale_error
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from engine.poteen.elements.basic.select import Select
from engine.poteen.error import ElementNotFoundException
from engine.poteen.log.resultList import ResultList
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from ..dialogs.environmentDeploymentModeDialog \
    import EnvironmentDeploymentModeDialog
from .listView import Cluster_Nodes_ListView
from ...cluster.generic.node import Node
from ...cluster.nodes.rolesPanel import RolesPanel


class Cluster_Nodes_View(AbstractView):
    def __init__(self, parent=None):
        self.addNodes = Link(
            xpath="//div//a[@class='btn btn-success btn-add-nodes']",
            element_name="Add nodes"
        )
        self.deleteNodes = Button(
            xpath="//button[contains(@class,'btn-delete-nodes')]",
            element_name="Delete nodes"
        )
        self.reassignRoles = Button(
            xpath="//button[contains(@class, 'btn-assign-roles')]"
                  "and contains(text(),'Reassign Roles')]",
            element_name="Reassign roles"
        )
        self.assignRoles = Button(
            xpath="//button[contains("
                  "@class, 'btn btn-success btn-assign-roles') "
                  "and contains(text(),'Assign Roles')]",
            element_name="Reassign roles"
        )
        self.environment_status = HtmlElement(
            xpath="//div[@class='environment-status']",
            element_name="Environment status"
        )
        self.groupBy = Select(
            xpath="//div[@class='cluster-toolbar-item nodes-filter']"
                  "//select[@name='grouping']",
            element_name="Select group by"
        )
        self.backToEnvironmentNodeList = Button(
            xpath="//div[@class='btn btn-go-to-cluster']",
            element_name="Back to Environment Node List"
        )

        self.compute_nodelist = Button(
            xpath="//div[@class='node-groups' and "
                  "contains(div[@class='row-fluid node-group-header']"
                  "//h4/text(),'compute')]",
            element_name="computes block"
        )
        self.controller_nodelist = HtmlElement(
            xpath="//div[@class='node-groups' and "
                  "contains(div[@class='row-fluid node-group-header']"
                  "//h4/text(),'controller')]",
            element_name="controllers block"
        )
        self.cinder_nodelist = Button(
            xpath="//div[@class='node-groups' and "
                  "contains(div[@class='row-fluid node-group-header']"
                  "//h4/text(),'cinder')]",
            element_name="cinders block"
        )
        self.deploymentMode = Button(
            xpath="//button[contains(@class,'btn btn-cluster-actions')]",
            element_name="Deployment mode"
        )
        self.alertError = HtmlElement(
            xpath="//div[contains(@class, 'alert-block') "
                  "and contains(@class, 'global-error')]/p",
            element_name="Alert Error"
        )

        AbstractView.__init__(self, parent)

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
            clickNext=True
        ))
        return rl

    @catch_stale_error
    def verify_cinder_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.cinder_nodelist.get_element()
        ).verify_nodes(*args)

    @catch_stale_error
    def verify_compute_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.compute_nodelist.get_element()
        ).verify_nodes(*args)

    @catch_stale_error
    def verify_controller_nodes(self, *args):
        return Cluster_Nodes_ListView(
            self.controller_nodelist.get_element()
        ).verify_nodes(*args)

    def get_nodes_controllers(self):
        return Cluster_Nodes_ListView(self.controller_nodelist.get_element()) \
            .get_nodes()

    def get_nodes_computes(self):
        return Cluster_Nodes_ListView(self.compute_nodelist.get_element()) \
            .get_nodes()

    def get_nodes_cinders(self):
        return Cluster_Nodes_ListView(self.cinder_nodelist.get_element()) \
            .get_nodes()

    def verify_controller_nodes_not_exist(self, *args):
        return Cluster_Nodes_ListView(
            self.compute_nodelist.get_element()
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
            if elements_names == "controllers":
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

    def verify_controllers_amount(self, value):
        return self.verify_amount("controllers", value)

    def verify_computes_amount(self, value):
        return self.verify_amount("computes", value)

    def verify_cinders_amount(self, value):
        return self.verify_amount("cinders", value)

    def select_nodes(self, role, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(Cluster_Nodes_ListView().node.find(
                name=name).get_element())
            rl.push(node.select())
        rl.push(RolesPanel().checkbox_role.find(role=role).set_value('on'))
        rl.push(self.apply())
        ActionBot().wait_for_time(2)
        WaitBot().wait_for_web_element_displays(
            Cluster_Nodes_View().environment_status)
        ActionBot().wait_for_time(2)
        return rl

    def select_nodes_2_roles(self, role1, role2, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(Cluster_Nodes_ListView().node.find(
                name=name).get_element())
            rl.push(node.select())
        rl.push(RolesPanel().checkbox_role.find(role=role1).set_value('on'))
        rl.push(RolesPanel().checkbox_role.find(role=role2).set_value('on'))
        rl.push(self.apply())
        ActionBot().wait_for_time(2)
        WaitBot().wait_for_web_element_displays(
            Cluster_Nodes_View().environment_status)
        ActionBot().wait_for_time(2)
        return rl

    def select_nodes_3_roles(self, role1, role2, role3, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(Cluster_Nodes_ListView().node.find(
                name=name).get_element())
            rl.push(node.select())
        rl.push(RolesPanel().checkbox_role.find(role=role1).set_value('on'))
        rl.push(RolesPanel().checkbox_role.find(role=role2).set_value('on'))
        rl.push(RolesPanel().checkbox_role.find(role=role3).set_value('on'))
        rl.push(self.apply())
        ActionBot().wait_for_time(2)
        WaitBot().wait_for_web_element_displays(
            Cluster_Nodes_View().environment_status)
        ActionBot().wait_for_time(2)
        return rl
