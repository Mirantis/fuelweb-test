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
        logger.info(CreateEnvironmentDialog().verify_releases_list(
            ['RHOS 3.0 for RHEL 6.4 (2013.1.2)',
             'Grizzly on CentOS 6.4 (2013.1.2)']))



    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_release_downloading(self):
        PoteenLogger.add_test_case(
            "Release downloading")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))

        # RHSM
        logger.info(CreateEnvironmentDialog().license_type.find(
            'rhsm').verify_value(True))
        logger.info(
            CreateEnvironmentDialog().red_hat_username.verify_visible(True))
        logger.info(
            CreateEnvironmentDialog().red_hat_password.verify_visible(True))
        logger.info(CreateEnvironmentDialog().create())
        logger.info(CreateEnvironmentDialog().alert_error.verify_attribute(
            'style', 'display: block;'))
        logger.info(CreateEnvironmentDialog().alert_error.verify_value(
            'All fields are required'))

        # RHN Satellite
        logger.info(CreateEnvironmentDialog().license_type.find(
            'rhn').click_and_wait())
        logger.info(
            CreateEnvironmentDialog().red_hat_username.verify_visible(True))
        logger.info(
            CreateEnvironmentDialog().red_hat_password.verify_visible(True))

        logger.info(CreateEnvironmentDialog(
        ).satellite_server_hostname.verify_visible(True))

        logger.info(CreateEnvironmentDialog(
        ).activation_key.verify_visible(True))

        logger.info(CreateEnvironmentDialog().create())
        logger.info(CreateEnvironmentDialog().alert_error.verify_attribute(
            'style', 'display: block;'))
        logger.info(CreateEnvironmentDialog().alert_error.verify_value(
            'All fields are required'))
