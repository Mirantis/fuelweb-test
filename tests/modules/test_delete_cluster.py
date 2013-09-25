from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView import Cluster_BrowseView
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.view import Cluster_Nodes_View
from ..components.settings import *

logger = PoteenLogger


class Test_Deployment(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Deployment, cls).setUpClass()
        PoteenLogger.add_test_suite("Delete cluster")

    @attr("test", set=["regression"])
    def test_delete_cluster_after_successful_deployment(self):
        PoteenLogger.add_test_case(
            "Delete cluster after successful deployment")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
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
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], ["Dell Inspiron"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'compute', "Dell Inspiron"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove("Test environment"))
        logger.info(Cluster_BrowseView().verify_clusters_amount(0))

    @attr(set=["regression"])
    @attr("skip")
    def test_can_not_add_offline_node(self):
        PoteenLogger.add_test_case(
            "Can not add 'offline' node to environment")

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

        logger.info(Cluster_Nodes_View().addNodes.click_and_wait())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], ["Supermicro X9SCD (offline)", "Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().verify_node_with_role_not_exists(
            'controller', "Supermicro X9SCD (offline)"
        ))
