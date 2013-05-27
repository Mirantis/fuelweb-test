from nose.plugins.attrib import attr
from engine.poteen.contextHolder import ContextHolder
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main

logger = PoteenLogger


class Test_Deployment(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Deployment, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")
        # ContextHolder.set_browser("firefox")
        # ContextHolder.set_do_screenshot(False)
        # ContextHolder.set_url("http://fuelweb.vm.mirantis.net:8000/")

    @attr(env=["fakeui"], set=["smoke", "regreaasion", "full"])
    def test_deploy_no_ha_1_controller_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 1 compute")
        # logger.info(Main().navigate())
