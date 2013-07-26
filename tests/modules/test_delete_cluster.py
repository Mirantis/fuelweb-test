from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView import Cluster_BrowseView
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from ..components.functionality.cluster.nodes.view import Cluster_Nodes_View
from ..components.settings import *
from base_test_case import BaseTestCase

logger = PoteenLogger


class Test_Deployment(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(Test_Deployment, cls).setUpClass()
        PoteenLogger.add_test_suite("Delete cluster")

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_delete_cluster_after_successful_deployment(self):
        PoteenLogger.add_test_case(
            "Delete cluster after successful deployment")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        self.create_environment(cluster_name, cluster_key,
                                Cluster.DEPLOYMENT_MODE_MULTI_NODE)
        self.add_nodes(1, 1)
        self.deploy_changes()
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove("Test environment"))
        logger.info(Cluster_BrowseView().verify_clusters_amount(0))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_can_not_add_offline_node(self):
        PoteenLogger.add_test_case(
            "Delete cluster with offline node")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        self.create_environment(cluster_name, cluster_key,
                                Cluster.DEPLOYMENT_MODE_MULTI_NODE)

        logger.info(Cluster_Nodes_View().click_add_controller())
        logger.info(Cluster_Nodes_ListView().click_nodes(
            "Supermicro X9SCD (offline)"
        ))
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Dell Inspiron"
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes_not_exist(
            "Supermicro X9SCD (offline)"
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron"
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
