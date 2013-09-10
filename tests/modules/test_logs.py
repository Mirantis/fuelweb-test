from nose.plugins.attrib import attr
from engine.poteen.bots.waitBot import WaitBot

from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from ..components.settings import OPENSTACK_CURRENT_VERSION
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.logs.view import Cluster_Logs_View


logger = PoteenLogger


class Test_Logs(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Logs, cls).setUpClass()
        PoteenLogger.add_test_suite("Logs validation")

    @attr(set=["smoke", "regression"])
    def test_show_logs(self):
        PoteenLogger.add_test_case(
            "Test show logs")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_View().click_logs_tab())
        logger.info(Cluster_Logs_View().set_log_filter(
            log="Admin node",
            source="REST API",
            level="DEBUG"
        ))
        logger.info(Cluster_Logs_View().show_button.click())
        logger.info(WaitBot().wait_loading())
        logger.info(Cluster_Logs_View().table_logs.verify_visible(True))
