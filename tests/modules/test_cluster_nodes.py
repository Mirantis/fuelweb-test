from engine.poteen.bots.verifyBot import VerifyBot
from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from ..components.settings \
    import OPENSTACK_CURRENT_VERSION, DEFAULT_DEPLOYMENT_TIMEOUT_UI
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.nodes.view import Cluster_Nodes_View

logger = PoteenLogger


class Test_Cluster_nodes(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Cluster_nodes, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster nodes testing")

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_form(self):
        PoteenLogger.add_test_case(
            "Testing cluster page")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(
            Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(VerifyBot().verify_disabled(
            Cluster_Nodes_View().deploymentMode.get_element(),
            None, "Link deployment mode"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addCompute.get_element(),
            True, "Add compute button"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addController.get_element(),
            True, "Add controller button"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addCinder.get_element(),
            True, "Add cinder button"))
        logger.info(
            Cluster_Nodes_View().verify_controllers_placeholders_amount(1))
        logger.info(Cluster_Nodes_View().verify_nodelists_visibility(True))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_cluster_deployment_mode_dialog(self):
        PoteenLogger.add_test_case(
            "Testing cluster deployment mode dialog")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(
            Cluster_Nodes_View().verify_controllers_placeholders_amount(3))
        logger.info(Cluster_Nodes_View().verify_nodelists_visibility(True))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_addition_node_controller_role(self):
        PoteenLogger.add_test_case(
            "Testing node addition to controller role")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(
            Cluster_Nodes_View().verify_controllers_placeholders_amount(0))
        logger.info(Cluster_Nodes_View().verify_controllers_amount(1))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_addition_node_compute_role(self):
        PoteenLogger.add_test_case(
            "Testing node addition to compute role")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_computes_amount(1))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_addition_node_cinder_role(self):
        PoteenLogger.add_test_case(
            "Testing node addition to cinder role")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_add_cinder())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_cinders_amount(1))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_deletion_node_scheduled_for_addition(self):
        PoteenLogger.add_test_case(
            "Testing deletion of compute node, scheduled for addition")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_computes_amount(1))
        logger.info(Cluster_Nodes_View().click_delete_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Pending Addition')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().verify_computes_amount(0))

    @attr(set=["smoke", "regression"])
    @attr("skip")
    def test_testing_deployment(self):
        PoteenLogger.add_test_case(
            "Testing deployment")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addControllerDisabled.get_element(),
            True, "Add controller disabled"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addComputeDisabled.get_element(),
            True, "Add compute disabled"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().addCinderDisabled.get_element(),
            True, "Add cinder disabled"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().deleteControllerDisabled.get_element(),
            True, "Delete controller disabled"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().deleteComputeDisabled.get_element(),
            True, "Delete compute disabled"))
        logger.info(VerifyBot().verify_visibility(
            Cluster_Nodes_View().deleteCinderDisabled.get_element(),
            True, "Delete cinder disabled"))
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))

    @attr(set=["regression"])
    @attr("skip")
    def test_delete_node_add_node_and_deploy(self):
        PoteenLogger.add_test_case(
            "Delete one node from environment after successful deployment. "
            "Add new nodes and deploy.")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_successful_deployment_per_name(cluster_name)
        )
        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().click_delete_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Ready')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:1]
        ))
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            *available_nodes_names[:2]
        ))
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
        logger.info(
            Cluster_View().verify_success_message("Successfully removed")
        )
        logger.info(Cluster_Nodes_View().verify_computes_amount(3))
        logger.info(Cluster_Nodes_View().verify_controllers_amount(1))
        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
