from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from ..components.functionality.main import Main
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.editView import Cluster_View
from base_test_case import BaseTestCase

logger = PoteenLogger


class Test_Deployment_HA_Mode(BaseTestCase):

    cluster_name = "Test environment"

    @classmethod
    def setUpClass(cls):
        super(Test_Deployment_HA_Mode, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster HA mode deployment")

    def deploy(self, cluster_name, controllers=0, computes=0):
        PoteenLogger.add_test_case(
            "Deploy in mode with HA ({controllers} controllers + "
            "{computes} compute nodes)".format(
                controllers=controllers, computes=computes))

        cluster_key = "cluster"

        logger.info(Main().navigate())
        self.create_environment(cluster_name, cluster_key,
                                Cluster.DEPLOYMENT_MODE_MULTI_NODE_WITH_HA)
        self.add_nodes(controllers, computes)
        self.deploy_changes()

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_2_controller(self):
        self.deploy(self.cluster_name, 2)
        logger.info(Cluster_View().verify_error_message(
            "Not enough controllers, ha mode requires at least 3 controllers"
        ))

    @attr(env=["vm"], set=["smoke", "regression", "full"])
    def test_vm_deploy_2_controller(self):
        self.bootstrap_nodes(self.ci().nodes().slaves[0:2])
        self.deploy(self.cluster_name, 2)
        logger.info(Cluster_View().verify_error_message(
            "Not enough controllers, ha mode requires at least 3 controllers"
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_3_controller_2_compute(self):
        self.deploy(self.cluster_name, 3, 2)
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))

    @attr(env=["vm"], set=["smoke", "regression", "full"])
    def test_vm_deploy_3_controller_2_compute(self):
        self.bootstrap_nodes(self.ci().nodes().slaves[0:5])
        self.deploy(self.cluster_name, 3, 2)
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_3_controller_4_compute(self):
        self.deploy(self.cluster_name, 3, 4)
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))

    @attr(env=["vm"], set=["smoke", "regression", "full"])
    def test_vm_deploy_3_controller_4_compute(self):
        self.bootstrap_nodes(self.ci().nodes().slaves[0:7])
        self.deploy(self.cluster_name, 3, 4)
        logger.info(Cluster_View().verify_successful_deployment_per_name(
            self.cluster_name
        ))
