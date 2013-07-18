from nose.plugins.attrib import attr

from engine.poteen.contextHolder import ContextHolder
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from tests.components.constants import TestConstants
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from tests.components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View

logger = PoteenLogger


class TestReleases(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestReleases, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_releases_page_layout(self):
        PoteenLogger.add_test_case(
            "Releases page layout")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        CreateEnvironmentDialog().verify_releases_list(
            ['RHOS 3.0 for RHEL 6.4 (2013.1.2)',
             'Grizzly on CentOS 6.4 (2013.1.2)'])



    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller_1_compute(self):
        PoteenLogger.add_test_case(
            "Verify environment version")

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
        logger.info(Cluster_Nodes_View().verify_version(TestConstants.OPENSTACK_CURRENT_VERSION))