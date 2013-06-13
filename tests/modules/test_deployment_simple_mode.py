from nose.plugins.attrib import attr

from engine.poteen.contextHolder import ContextHolder
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
from ..components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from ..components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View

logger = PoteenLogger


class TestDeploymentSimpleMode(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestDeploymentSimpleMode, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")
        # ContextHolder.set_browser("firefox")
        # ContextHolder.set_do_screenshot(False)
        # ContextHolder.set_url("http://127.0.0.1:8000/")

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 1 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Dell Inspiron"
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Dell Inspiron"
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller_3_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 3 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Dell Inspiron", "Supermicro X9SCD", "KVM"
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron", "Supermicro X9SCD", "KVM"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller_4_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 4 compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Dell Inspiron", "Supermicro X9SCD", "KVM", "VirtualBox"
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron", "Supermicro X9SCD", "KVM", "VirtualBox"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_deploy_no_ha_1_controller_2_compute_1_offline_compute(self):
        PoteenLogger.add_test_case(
            "Deploy without HA mode 1 controller 2 compute 1 offline compute")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Dell Inspiron", "Supermicro X9SCD",
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            "Supermicro X9DRW"
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron", "Supermicro X9SCD",
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT
        ))
        logger.info(Cluster_View().verify_success_message(
            "Deployment of environment {name} is done."
            " Access WebUI of OpenStack"
            .format(name=cluster_name)
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        logger.info(Cluster_Nodes_ListView().select_nodes(
            "Supermicro X9SCD (offline)",
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            "Dell Inspiron", "Supermicro X9SCD", "Supermicro X9SCD (offline)"
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_Nodes_View().verify_error_contains(
            "Supermicro X9SCD (offline)", "is offline. Remove it from "
                                          "environment and try again."))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
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
            logger.info(
                Cluster_BrowseView().click_add_new_cluster(cluster_key)
            )
            logger.info(CreateEnvironmentDialog().populate(
                name=cluster_info['name'],
                version=OPENSTACK_CURRENT_VERSION,
                submit=True
            ))
            logger.info(Cluster_BrowseView().select_by_key(cluster_key))
            logger.info(Cluster_Nodes_View().select_environment_mode(
                deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
            ))
            logger.info(Cluster_Nodes_View().click_add_controller())
            logger.info(Cluster_Nodes_ListView().select_nodes(
                *cluster_info['controllers']
            ))
            logger.info(Cluster_Nodes_View().click_add_compute())
            logger.info(Cluster_Nodes_ListView().select_nodes(
                *cluster_info['computes']
            ))
            logger.info(Cluster_Nodes_View().verify_controller_nodes(
                *cluster_info['controllers']
            ))
            logger.info(Cluster_Nodes_View().verify_compute_nodes(
                *cluster_info['computes']
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
                DEFAULT_DEPLOYMENT_TIMEOUT
            ))
            logger.info(Cluster_View().verify_success_message(
                "Deployment of environment {name} is done."
                " Access WebUI of OpenStack"
                .format(name=cluster_info['name'])
            ))
