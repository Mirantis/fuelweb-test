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


class Test_Deployment_With_Cinder(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Deployment_With_Cinder, cls).setUpClass()
        PoteenLogger.add_test_suite("Deployment with cinder")

    @attr(set=["regression"])
    def test_deploy_no_ha_1_cinder(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 1 compute 1 cinder")

        cluster_key = "cluster"
        cluster_name = "Test simple deployment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_cinder())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
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
            "Ready", 3))

    @attr(set=["regression"])
    def test_deploy_HA_1_cinder(self):
        PoteenLogger.add_test_case(
            "Deploy HA mode 3 controllers 1 compute 1 cinder")

        cluster_key = "cluster"
        cluster_name = "Test simple deployment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE_WITH_HA
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:3]
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_cinder())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
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
            "Ready", 5))
