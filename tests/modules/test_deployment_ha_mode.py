from nose.plugins.attrib import attr
from engine.poteen.bots.verifyBot import VerifyBot
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


class Test_Deployment_HA_Mode(TestCasePoteen):

    cluster_name = "Test environment"

    @classmethod
    def setUpClass(cls):
        super(Test_Deployment_HA_Mode, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster HA mode deployment")

    def deploy(self, cluster_name, controllers=1, computes=0):
        PoteenLogger.add_test_case(
            "Deploy in mode with HA ({controllers} controllers + "
            "{computes} compute nodes)".format(
                controllers=controllers, computes=computes))

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE_WITH_HA
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:controllers]
        ))

        if computes > 0:
            logger.info(Cluster_Nodes_View().click_add_nodes())
            logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
                ['compute'],
                available_nodes_names[controllers:controllers + computes]
            ))

        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', available_nodes_names[:controllers]
        ))
        if computes > 0:
            logger.info(Cluster_Nodes_View().verify_nodes(
                'compute',
                available_nodes_names[controllers:controllers + computes]
            ))

        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))

    @attr(set=["regression"])
    def test_deploy_2_controller(self):
        PoteenLogger.add_test_case(
            "Deploy in mode with HA ({controllers} controllers + "
            "{computes} compute nodes)".format(
                controllers=2, computes=0))

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE_WITH_HA
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], available_nodes_names[:2]
        ))

        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', *available_nodes_names[:2]
        ))

        logger.info(Cluster_View().click_deploy_changes())
        logger.info(VerifyBot().verify_visibility(
            DeployChangesDialog().alert_message.get_element(),
            True, 'Alert message'))
        logger.info(VerifyBot().verify_contains(
            'disabled', DeployChangesDialog().deploy_button().get_element()
            .get_attribute('class'), 'Deploy button'))

    @attr("test",set=["regression"])
    def test_deploy_3_controller_2_compute(self):
        self.deploy(self.cluster_name, 3, 2)
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))

    @attr(set=["regression"])
    def test_deploy_3_controller_4_compute(self):
        self.deploy(self.cluster_name, 3, 4)
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))
