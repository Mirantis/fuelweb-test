
from nose.plugins.attrib import attr

from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from ..components.settings import *
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from ..components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View

logger = PoteenLogger


class TestRedeployment(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestRedeployment, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")

    @attr(set=["regression"])
    def test_redeployment_after_addition_new_compute_node(self):
        PoteenLogger.add_test_case(
            "Redeployment after addition new compute node")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_nodes())
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
            Cluster_View().verify_successful_deployment_per_name(
                "Test environment")
        )
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Ready', 2))
        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Pending Addition', 1))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Ready', 2))
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(
                "Test environment")
        )
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Ready', 3))

    @attr(set=["regression"])
    def test_redeployment_after_deletion_node(self):
        PoteenLogger.add_test_case(
            "Redeployment after deletion node")

        cluster_key = "cluster"
        cluster_name = "Test simple deployment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], available_nodes_names[:2]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Ready', 3))
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Ready')
        logger.info(
            Cluster_Nodes_View().delete_nodes(*available_nodes_names[:1]))
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Pending Deletion', 1))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_Nodes_ListView().verify_amount_nodes_in_status(
            'Ready', 2))
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_success_message("Successfully removed")
        )
        logger.info(Cluster_Nodes_View().verify_amount('compute', 1))
        logger.info(Cluster_Nodes_View().verify_amount('controller', 1))
