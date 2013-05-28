from nose.plugins.attrib import attr
from engine.poteen.contextHolder import ContextHolder
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from tests.components.constants import TestConstants
from tests.components.functionality.cluster.browseView import Cluster_BrowseView
from tests.components.functionality.cluster.cluster import Cluster
from tests.components.functionality.cluster.dialogs.createEnvironmentDialog import CreateEnvironmentDialog
from tests.components.functionality.cluster.dialogs.deployChangesDialog import DeployChangesDialog
from tests.components.functionality.cluster.editView import Cluster_View
from tests.components.functionality.cluster.nodes.listView import Cluster_Nodes_ListView
from tests.components.functionality.cluster.nodes.view import Cluster_Nodes_View

logger = PoteenLogger


class Test_Deployment(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Deployment, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")
        # ContextHolder.set_browser("firefox")
        # ContextHolder.set_do_screenshot(False)
        # ContextHolder.set_url("http://172.18.76.52:8000/")

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 1 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=TestConstants.OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentType=Cluster.DEPLOYMENT_TYPE_COMPUTE_ONLY,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
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
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            TestConstants.DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))