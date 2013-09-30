from engine.poteen.bots.verifyBot import VerifyBot
from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from ..components.settings \
    import OPENSTACK_CURRENT_VERSION, DEFAULT_DEPLOYMENT_TIMEOUT_UI
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.nodes.view import Cluster_Nodes_View

logger = PoteenLogger


class Test_Cluster_nodes(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Cluster_nodes, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster nodes testing")

    @attr(set=["smoke", "regression"])
    def test_form(self):
        PoteenLogger.add_test_case(
            "Testing cluster page")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(
            Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addNodes.get_element(),
            True, "Add nodes button"))
        logger.info(VerifyBot().verify_disabled(
            Cluster_Nodes_View().deleteNodes.get_element(),
            'true', "Delete nodes button"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().environment_status.get_element(),
            True, "Environment status"))
        logger.info(VerifyBot().verify_disabled(
            Cluster_Nodes_View().groupBy.get_element(),
            'true', "Group by select"))

    @attr(set=["smoke", "regression"])
    def test_addition_node_controller_role(self):
        PoteenLogger.add_test_case(
            "Testing node addition to controller role")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_amount('controller', 1))

    @attr(set=["smoke", "regression"])
    def test_addition_node_compute_role(self):
        PoteenLogger.add_test_case(
            "Testing node addition to compute role")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_amount('compute', 1))

    @attr(set=["smoke", "regression"])
    def test_addition_node_cinder_role(self):
        PoteenLogger.add_test_case(
            "Testing node addition to cinder role")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['cinder'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_amount('cinder', 1))

    @attr(set=["smoke", "regression"])
    def test_deletion_node_scheduled_for_addition(self):
        PoteenLogger.add_test_case(
            "Testing deletion of compute node, scheduled for addition")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_amount('compute', 1))
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Pending Addition')
        logger.info(Cluster_Nodes_View().delete_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_amount('compute', 0))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_testing_deployment(self):
        PoteenLogger.add_test_case(
            "Testing deployment")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:1]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(VerifyBot().verify_disabled(
            Cluster_Nodes_View().addNodes.get_element(),
            'true', "Add node button is disabled"))
        logger.info(VerifyBot().verify_disabled(
            Cluster_Nodes_View().deleteNodes.get_element(),
            'true', "Delete node button is disabled"))
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))

    @attr(set=["regression"])
    def test_delete_node_add_node_and_deploy(self):
        PoteenLogger.add_test_case(
            "Delete one node from environment after successful deployment. "
            "Add new nodes and deploy.")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": cluster_name,
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], available_nodes_names[:1]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name))
        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Ready')
        logger.info(
            Cluster_Nodes_View().delete_nodes(*available_nodes_names[:1]))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:1]))
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], available_nodes_names[:2]))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_success_message("Successfully removed"))
        logger.info(Cluster_Nodes_View().verify_amount('compute', 2))
        logger.info(Cluster_Nodes_View().verify_amount('controller', 1))
