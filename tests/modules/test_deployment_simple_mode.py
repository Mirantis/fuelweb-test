from nose.plugins.attrib import attr
from engine.poteen.bots.verifyBot import VerifyBot

from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from ..components.settings import *
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View

logger = PoteenLogger


class TestDeploymentSimpleMode(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestDeploymentSimpleMode, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")

    @attr(set=["smoke", "regression"])
    def test_deploy_no_ha_1_controller_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 1 compute")

        cluster_key = "cluster"
        cluster_name = "Test simple deployment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": cluster_name,
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], ["Dell Inspiron"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'compute', ["Dell Inspiron"]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )

    @attr(set=["regression"])
    def test_deploy_no_ha_1_controller(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

         # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": cluster_name,
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )

    @attr(set=["regression"])
    def test_deploy_no_ha_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 compute")

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

        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], ["Dell Inspiron"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'compute', ["Dell Inspiron"]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(VerifyBot().verify_contains(
            'disabled', DeployChangesDialog().deploy_button().get_element()
            .get_attribute('class'), 'Deploy button'))
        logger.info(VerifyBot().verify_visibility(
            DeployChangesDialog().alert_message.get_element(),
            True, "Alert error message"))

    @attr(set=["regression"])
    def test_deploy_no_ha_1_controller_3_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 3 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": cluster_name,
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], ["Supermicro X9DRW"]
        ))

        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], ["Dell Inspiron", "Supermicro X9SCD", "KVM"]
        ))

        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'compute', ["Dell Inspiron", "Supermicro X9SCD", "KVM"]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )

    @attr(set=["regression"])
    def test_deploy_no_ha_1_controller_4_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 4 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

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
        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().click_add_nodes())
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'],
            ["Dell Inspiron", "Supermicro X9SCD", "KVM", "VirtualBox"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', ["Supermicro X9DRW"]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'compute',
            ["Dell Inspiron", "Supermicro X9SCD", "KVM", "VirtualBox"]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )

    @attr(set=["regression"])
    def test_deploy_concurrent_deployment_3_environments(self):
        PoteenLogger.add_test_case(
            "Concurrent simple deployment 3 environments")

        clusters = {
            "cluster1": {
                "name": "Test environment 1",
                "controllers": ["VirtualBox"],
                "computes": ["Supermicro X9DRW"]
            },
            "cluster2": {
                "name": "Test environment 2",
                "controllers": ["Supermicro X9SCD"],
                "computes": ["KVM"]
            },
            "cluster3": {
                "name": "Test environment 3",
                "controllers": ["Dell Inspiron"],
                "computes": ["Supermicro X9DRW (srv07)"]
            }
        }

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        for cluster_key, cluster_info in clusters.iteritems():
            logger.info(Main().navigate())

            # create cluster
            logger.info(Cluster_BrowseView().click_add_new_cluster(
                cluster_key))
            logger.info(CreateEnvironmentDialog().create_environment(
                {
                    "name": "Test environment",
                    "version": OPENSTACK_CURRENT_VERSION,
                    "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
                }
            ))
            logger.info(Cluster_BrowseView().select_by_key(cluster_key))

            logger.info(Cluster_Nodes_View().click_add_nodes())
            logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
                ['controller'], cluster_info['controllers']
            ))
            logger.info(Cluster_Nodes_View().click_add_nodes())
            logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
                ['compute'], cluster_info['computes']
            ))
            logger.info(Cluster_Nodes_View().verify_nodes(
                'controller', cluster_info['controllers']
            ))
            logger.info(Cluster_Nodes_View().verify_nodes(
                'compute', cluster_info['computes']
            ))

        for cluster_key, cluster_info in clusters.iteritems():
            logger.info(Main().navigate())
            logger.info(Cluster_BrowseView().select_by_key(cluster_key))
            logger.info(Cluster_View().click_deploy_changes())
            logger.info(DeployChangesDialog().deploy())

        for cluster_key, cluster_info in clusters.iteritems():
            logger.info(Main().navigate())
            logger.info(Cluster_BrowseView().select_by_key(cluster_key))
            logger.info(Cluster_View().wait_deployment_done(
                DEFAULT_DEPLOYMENT_TIMEOUT_UI
            ))
            logger.info(
                Cluster_View().verify_successful_deployment_per_name(
                    cluster_info['name']
                )
            )
