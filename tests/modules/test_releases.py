from nose.plugins.attrib import attr

from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from ..components.functionality.main import Main
from ..components.functionality.releases.tables.releasesTable \
    import Releases_Table
from ..components.navigation.mainMenu import Main_Menu
from ..components.settings \
    import RELEASE_RHOS, RELEASE_GRIZZLY_CENTOS, RELEASE_GRIZZLY_UBUNTU
from ..components.functionality.releases.dialogs.configureReleaseDialog\
    import Configure_Release_Dialog


logger = PoteenLogger


class Test_Releases(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Releases, cls).setUpClass()
        PoteenLogger.add_test_suite("Test releases functionality")

    @attr(set=["smoke", "regression"])
    def test_releases(self):
        PoteenLogger.add_test_case(
            "Test releases page")

        logger.info(Main().navigate())
        logger.info(Main_Menu().releases.click())
        logger.info(Releases_Table().verify_releases_count(3))
        logger.info(Releases_Table().verify_release_status(
            RELEASE_GRIZZLY_CENTOS, "Active"))
        logger.info(Releases_Table().verify_release_status(
            RELEASE_GRIZZLY_UBUNTU, "Active"))
        if Releases_Table().verify_release_status(
                RELEASE_RHOS, "Not available").i_passed():
            logger.info(Releases_Table().click_configure(RELEASE_RHOS))
            logger.info(Configure_Release_Dialog().licence_rhn.click())
            logger.info(
                Configure_Release_Dialog().licence_rhn.verify_value(True))
            logger.info(
                Configure_Release_Dialog().verify_controls_presence("RHN")
            )
            logger.info(Configure_Release_Dialog().licence_rhsm.click())
            logger.info(
                Configure_Release_Dialog().licence_rhsm.verify_value(True))
            logger.info(
                Configure_Release_Dialog().verify_controls_presence("RHSM")
            )
            logger.info(Configure_Release_Dialog().populate(
                "rheltest", "password"))
            logger.info(Configure_Release_Dialog().download())
            logger.info(Releases_Table().wait_downloading(RELEASE_RHOS))
            logger.info(Releases_Table().verify_release_status(
                RELEASE_RHOS, "Active"))
        else:
            logger.info(Releases_Table().verify_release_status(
                RELEASE_RHOS, "Active"))
