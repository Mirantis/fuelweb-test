from nose.plugins.attrib import attr
from engine.poteen.contextHolder import ContextHolder
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


class TestDeploymentHAMode(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestDeploymentHAMode, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")
        ContextHolder.set_browser("firefox")
        ContextHolder.set_do_screenshot(False)
        ContextHolder.set_url("http://localhost:8000/")

    def deploy(self, controllers=0, computes=0):
        PoteenLogger.add_test_case(
            "Deploy in mode with HA ({controllers} controllers + "
            "{computes} compute nodes)".format(
                controllers=controllers, computes=computes))

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
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

        if controllers > 0:
            logger.info(Cluster_Nodes_View().click_add_controller())
            available_nodes_names = Cluster_Nodes_ListView()\
                .get_nodes_names_by_status('Discovered')
            logger.info(Cluster_Nodes_ListView().select_nodes(
                *available_nodes_names[:controllers]
            ))

        if computes > 0:
            logger.info(Cluster_Nodes_View().click_add_compute())
            logger.info(Cluster_Nodes_ListView().select_nodes(
                *available_nodes_names[controllers:controllers + computes]
            ))

        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            *available_nodes_names[:controllers]
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            *available_nodes_names[controllers:controllers + computes]
        ))

        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_2_controller(self):
        self.deploy(2)

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_3_controller_2_compute(self):
        self.deploy(3, 2)

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_3_controller_4_compute(self):
        self.deploy(3, 4)

