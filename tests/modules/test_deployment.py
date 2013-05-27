from nose.plugins.attrib import attr
from engine.poteen.contextHolder import ContextHolder
from engine.poteen.log.result import Result
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from tests.components.functionality.cluster.browseView import Cluster_BrowseView
from tests.components.functionality.cluster.cluster import Cluster
from tests.components.functionality.cluster.dialogs.createEnvironmentDialog import CreateEnvironmentDialog
from tests.components.functionality.cluster.nodes.listView import Cluster_Nodes_ListView
from tests.components.functionality.cluster.nodes.view import Cluster_Nodes_View

logger = PoteenLogger


class Test_Deployment(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Deployment, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")
        ContextHolder.set_browser("firefox")
        ContextHolder.set_do_screenshot(False)
        ContextHolder.set_url("http://172.18.76.52:8000/")

    @attr(env=["fakeui"], set=["smoke", "regreaasion", "full"])
    def test_deploy_no_ha_1_controller_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 1 compute")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name="Test environment",
            version="Folsom",
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
        # logger.info()