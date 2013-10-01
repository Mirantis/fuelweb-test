from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.decorators import catch_stale_error
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link
from engine.poteen.elements.basic.select import Select
from engine.poteen.error import ElementNotFoundException
from engine.poteen.log.resultList import ResultList
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from .listView import Cluster_Nodes_ListView
from ...cluster.generic.node import Node
from ...cluster.nodes.rolesPanel import RolesPanel
from ...cluster.dialogs.deleteNodeDialog import DeleteNodeDialog
from tests.components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog


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
            element_name="Assign roles"
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

        self.nodelist = HtmlElement(
            xpath="//div[@class='node-groups' and "
                  "contains(div[@class='row-fluid node-group-header']"
                  "//h4/text(),'{role}')]",
            element_name="'{role}' block"
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

    @catch_stale_error
    def click_add_nodes(self):
        return self.addNodes.click_and_wait()

    def select_environment_mode(self, deploymentMode):
        rl = ResultList(
            "Select environment mode [{mode}]".format(
                mode=deploymentMode)
        )
        rl.push(self.click_deployment_mode())
        rl.push(CreateEnvironmentDialog().select_deployment_mode(
            deploymentMode
        ))
        rl.push(CreateEnvironmentDialog().clickNext())
        return rl

    @catch_stale_error
    def verify_nodes(self, role, nodes):
        return Cluster_Nodes_ListView(
            self.nodelist.find(role=role).get_element()
        ).verify_nodes(*nodes)

    def get_nodes(self, role):
        return Cluster_Nodes_ListView(
            self.nodelist.find(role=role).get_element()).get_nodes()

    def verify_node_with_role_not_exists(self, role, *args):
        return Cluster_Nodes_ListView(
            self.nodelist.find(role=role).get_element()
        ).verify_nodes_not_exist(*args)

    def verify_error_contains(self, *args):
        rl = ResultList("Verify error alert contains")
        for string in args:
            rl.push(Result(
                "String [{string}] exists".format(string=string),
                self.alertError.get_value().find(string) != -1
            ))
        return rl

    def verify_nodelists_visibility(self, value, *roles):
        rl = ResultList("Verify node lists visibility")
        for role in roles:
            rl.push(VerifyBot().verify_visibility(
                self.nodelist.find(role=role).get_element(),
                value, "'{role}' nodelist"))
        return rl

    def verify_amount(self, elements_role, value):
        result = None
        try:
            elements = self.get_nodes(role=elements_role)

            if value == 0:
                result = Result(
                    "Verify if amount of {role} is 0".format(
                        role=elements_role, value=value),
                    VerifyBot().verify_visibility(
                        elements, False, elements_role).i_passed())
            else:
                result = Result(
                    "Verify if amount of {role} is {value}".format(
                        role=elements_role, value=value),
                    len(elements) == value)

        except ElementNotFoundException:
            if value == 0:
                result = Result("There are no {name}".format(
                    role=elements_role), True)
        return result

    def select_nodes(self, *args):
        rl = ResultList("Select nodes")
        for name in args:
            node = Node(Cluster_Nodes_ListView().node.find(
                name=name).get_element())
            rl.push(node.select())
        return rl

    def select_roles(self, *roles):
        rl = ResultList("Select roles")
        for role in roles:
            rl.push(RolesPanel().checkbox_role.find(role=role).set_value('on'))
        return rl

    def assign_roles_to_nodes(self, roles, node_names):
        rl = ResultList("Select nodes and assign roles")
        rl.push(self.select_nodes(*node_names))
        rl.push(self.select_roles(*roles))
        rl.push(self.apply())
        ActionBot().wait_for_time(2)
        return rl

    def delete_nodes(self, *args):
        rl = ResultList("Delete nodes")
        rl.push(self.select_nodes(*args))
        rl.push(self.deleteNodes.click_and_wait())
        rl.push(DeleteNodeDialog().delete())
        return rl
