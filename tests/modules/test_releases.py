from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from tests.components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View
from tests.components.functionality.releases.browse_view \
    import Releases_BrowseView
from tests.components.functionality.releases.red_hat_account_dialog \
    import RedHatAccountDialog
from tests.components.settings import OPENSTACK_RHOS

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
    def test_rhos_creating(self):
        PoteenLogger.add_test_case(
            "Release downloading")

        cluster_key = "cluster"
        cluster_name = "Test"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_RHOS
        ))

        # RHSM
        logger.info(CreateEnvironmentDialog().license_type.find(
            value='rhsm').verify_value(True))
        logger.info(
            CreateEnvironmentDialog().red_hat_username.verify_visible(True))
        logger.info(
            CreateEnvironmentDialog().red_hat_password.verify_visible(True))
        logger.info(CreateEnvironmentDialog().create())
        logger.info(CreateEnvironmentDialog().inline_help.find(
            'Invalid username').verify_visible(True))
        logger.info(CreateEnvironmentDialog().inline_help.find(
            'Invalid password').verify_visible(True))

        # RHN Satellite
        logger.info(CreateEnvironmentDialog().license_type.find(
            value='rhn').click_and_wait())
        logger.info(
            CreateEnvironmentDialog().red_hat_username.verify_visible(True))
        logger.info(
            CreateEnvironmentDialog().red_hat_password.verify_visible(True))

        logger.info(CreateEnvironmentDialog(
        ).satellite_server_hostname.verify_visible(True))

        logger.info(CreateEnvironmentDialog(
        ).activation_key.verify_visible(True))

        logger.info(CreateEnvironmentDialog().create())
        logger.info(CreateEnvironmentDialog().inline_help.find(
            'Invalid username').verify_visible(True))
        logger.info(CreateEnvironmentDialog().inline_help.find(
            'Invalid password').verify_visible(True))
        logger.info(CreateEnvironmentDialog().inline_help.find(
            'Only valid fully qualified domain').verify_visible(True))
        logger.info(CreateEnvironmentDialog().inline_help.find(
            'Invalid activation key').verify_visible(True))

        logger.info(CreateEnvironmentDialog().license_type.find(
            value='rhsm').click_and_wait())
        logger.info(CreateEnvironmentDialog().red_hat_username.set_value(
            'rheltest'))
        logger.info(CreateEnvironmentDialog().red_hat_password.set_value(
            'password'))
        logger.info(CreateEnvironmentDialog().create())

        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().progress_bar.verify_visible())
        logger.info(Cluster_Nodes_View().wait_for_progress_bar_disappears())

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_release_downloading(self):
        PoteenLogger.add_test_case(
            "Release downloading")

        logger.info(Main().navigate())
        logger.info(Main().releases.click())
        logger.info(Releases_BrowseView().release_name.find(
            name='Grizzly on CentOS 6.4').verify_visible())
        logger.info(Releases_BrowseView().release_name.find(
            name='RHOS 3.0 for RHEL 6.4').verify_visible())
        logger.info(Releases_BrowseView().release_status.find(
            name='RHOS 3.0 for RHEL 6.4').verify_value(' Not available'))

        logger.info(Releases_BrowseView().configure.find(
            name='RHOS 3.0 for RHEL 6.4').click_and_wait())

        logger.info(RedHatAccountDialog().red_hat_username.set_value(
            'rheltest'))
        logger.info(RedHatAccountDialog().red_hat_password.set_value(
            'password'))
        logger.info(RedHatAccountDialog().download())

        logger.info(
            Releases_BrowseView().wait_for_progress_bar_disappears('RHOS'))

        logger.info(Releases_BrowseView().release_status.find(
            name='RHOS 3.0 for RHEL 6.4').verify_value(' Active'))
