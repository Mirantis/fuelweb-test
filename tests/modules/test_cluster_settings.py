from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from nose.plugins.attrib import attr

from ..components.settings import OPENSTACK_CURRENT_VERSION
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.confirmLeavePageDialog \
    import ConfirmLeavePageDialog
from ..components.functionality.cluster.openstack_settings.view \
    import OpenstackSettingsView

logger = PoteenLogger


class Test_OpenStack_settings(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_OpenStack_settings, cls).setUpClass()
        PoteenLogger.add_test_suite("OpenStack settings validation")

    @attr(set=["smoke", "regression"])
    def test_form(self):
        PoteenLogger.add_test_case(
            "Check openstack settings page")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_View().click_openstack_settings_tab())
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().load_defaults.get_element(),
            None, "Load defaults button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().cancel_changes.get_element(),
            'true', "Cancel changes button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().save_settings.get_element(),
            'true', "Save settings button"))
        logger.info(OpenstackSettingsView().show_password.click())
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().cancel_changes.get_element(),
            'true', "Cancel changes button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().save_settings.get_element(),
            'true', "Save settings button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().load_defaults.get_element(),
            None, "Load defaults button"))
        logger.info(VerifyBot().verify_visibility(
            OpenstackSettingsView().show_password_off.get_element(),
            True, "Show password button off"))
        logger.info(OpenstackSettingsView().show_password.click())
        logger.info(VerifyBot().verify_visibility(
            OpenstackSettingsView().show_password_on.get_element(),
            True, "Show password button on"))

        logger.info(OpenstackSettingsView().set_parameter_input(
            "username", "test name"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().load_defaults.get_element(),
            None, "Load defaults button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().save_settings.get_element(),
            None, "Save settings button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().cancel_changes.get_element(),
            None, "Cancel changes button"))

        logger.info(OpenstackSettingsView().set_parameter_input(
            "username", "admin"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().load_defaults.get_element(),
            None, "Load defaults button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().save_settings.get_element(),
            'true', "Save settings button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().cancel_changes.get_element(),
            'true', "Cancel changes button"))
        logger.info(OpenstackSettingsView().set_parameter_input(
            "username", "test name"))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(ConfirmLeavePageDialog().click_stay_on_page())
        ConfirmLeavePageDialog().wait_closing()
        logger.info(OpenstackSettingsView().cancel_changes.click_and_wait())
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().save_settings.get_element(),
            'true', "Save settings button"))

        logger.info(OpenstackSettingsView().set_parameter_input(
            "username", "test name"))
        logger.info(OpenstackSettingsView().save_settings.click_and_wait())
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().cancel_changes.get_element(),
            'true', "Cancel changes button"))

        logger.info(OpenstackSettingsView().load_defaults.click_and_wait())
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().cancel_changes.get_element(),
            None, "Cancel changes button"))
        logger.info(VerifyBot().verify_disabled(
            OpenstackSettingsView().save_settings.get_element(),
            None, "Save settings button"))
