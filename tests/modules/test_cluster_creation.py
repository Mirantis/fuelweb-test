from selenium.webdriver.common.by import By
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from nose.plugins.attrib import attr

from ..components.settings \
    import OPENSTACK_RHOS, OPENSTACK_GRIZZLY
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog

logger = PoteenLogger


class Test_Cluster_creation(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Cluster_creation, cls).setUpClass()
        PoteenLogger.add_test_suite("Network validation")

    @attr(set=["smoke", "regression"])
    def test_form(self):
        PoteenLogger.add_test_case(
            "Check environment creation page")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populateRHOS(
            name="Test environment",
            version=OPENSTACK_RHOS,
            downloadMode="rhn",
            username="rheltest",
            password="password",
            serverHostName="satellite server hostname",
            activationKey="activation key",
            submit=False
        ))

    @attr(set=["smoke", "regression"])
    def test_form_creation_with_grizzly(self):
        PoteenLogger.add_test_case(
            "Check creation page with grizzly")

        cluster_key = "cluster"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(
            CreateEnvironmentDialog().name.set_value("Test environment"))
        logger.info(WaitBot().wait_loading())
        logger.info(
            CreateEnvironmentDialog().version.set_value(OPENSTACK_GRIZZLY))
        logger.info(CreateEnvironmentDialog().name.click())
        WaitBot().wait_for_stop_resizing(
            By.XPATH, CreateEnvironmentDialog().XPATH_DIALOG)
        logger.info(VerifyBot().verify_visibility(
            CreateEnvironmentDialog().instruction.get_element(),
            False, "Instruction for RHOS"))
        logger.info(
            CreateEnvironmentDialog().version.set_value(OPENSTACK_RHOS))
        logger.info(CreateEnvironmentDialog().name.click())
        WaitBot().wait_for_stop_resizing(
            By.XPATH, CreateEnvironmentDialog().XPATH_DIALOG)
        logger.info(VerifyBot().verify_visibility(
            CreateEnvironmentDialog().instruction.get_element(),
            True, "Instruction for RHOS"))
        logger.info(
            CreateEnvironmentDialog().version.set_value(OPENSTACK_GRIZZLY))
        logger.info(CreateEnvironmentDialog().name.click())
        WaitBot().wait_for_stop_resizing(
            By.XPATH, CreateEnvironmentDialog().XPATH_DIALOG)
        logger.info(VerifyBot().verify_visibility(
            CreateEnvironmentDialog().instruction.get_element(),
            False, "Instruction for RHOS"))
