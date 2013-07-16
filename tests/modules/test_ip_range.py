from tests.components.functionality.cluster.network_settings.view \
    import NetworkSettingsView
from tests.components.settings import OPENSTACK_CURRENT_VERSION

__author__ = 'kcherchenko'

from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.cluster import Cluster
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.editView import Cluster_View
from ..components.functionality.cluster.nodes.view import Cluster_Nodes_View

logger = PoteenLogger


class Test_Network_settings(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Network_settings, cls).setUpClass()
        PoteenLogger.add_test_suite("Network validation")

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_form(self):
        PoteenLogger.add_test_case(
            "Check network settings page")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().
        click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().
        select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("on"))
        logger.info(NetworkSettingsView().verify_VLAN_manager_value("off"))
        logger.info(NetworkSettingsView().verify_amount_of_blocks(5))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
            .cancel_changes.get_element(), 'true', "Cancel changes button"))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
            .save_settings.get_element(), 'true', "Save settings button"))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
            .verify_networks.get_element(), None, "Verify networks button"))
        default_value = NetworkSettingsView().vm_networks_cidr.get_value()
        logger.info(NetworkSettingsView().vm_networks_cidr
        .set_value("240.0.1.0/25"))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
                .save_settings.get_element(), None, "Save settings button"))
        logger.info(NetworkSettingsView().vm_networks_cidr
                                        .set_value(default_value))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
            .save_settings.get_element(), 'true', "Save settings button"))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_change_network(self):
        PoteenLogger.add_test_case(
            "Change network manager")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().
        click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().
        select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("on"))
        logger.info(NetworkSettingsView().verify_VLAN_manager_value("off"))
        logger.info(NetworkSettingsView()
        .verify_visibility_vlan_manager_fields(False))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
            .save_settings.get_element(), 'true', "Save settings button"))
        logger.info(NetworkSettingsView().set_VLAN_manager("on"))
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("off"))
        logger.info(NetworkSettingsView().verify_disabled(NetworkSettingsView()
                .save_settings.get_element(), None, "Save settings button"))
        logger.info(NetworkSettingsView()
                .verify_visibility_vlan_manager_fields(True))
        logger.info(NetworkSettingsView().set_flatDHCP_manager("on"))
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("off"))
        logger.info(NetworkSettingsView()
        .verify_visibility_vlan_manager_fields(False))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_amount_field_validation(self):
        PoteenLogger.add_test_case(
            "Check Amount field validation")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().
        click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().
        select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().set_VLAN_manager("on"))
        logger.info(NetworkSettingsView().verify_error_amount(" ", False))
        logger.info(NetworkSettingsView().verify_error_amount("-10", False))
        logger.info(NetworkSettingsView().verify_error_amount("0", False))
        logger.info(NetworkSettingsView()
        .verify_error_amount("2", False, "4094"))
        logger.info(NetworkSettingsView()
        .verify_error_amount("2", True, "4093", "4094"))
        logger.info(NetworkSettingsView()
        .verify_error_amount("4094", True, "1", "4094"))
        logger.info(NetworkSettingsView()
        .verify_error_amount("10", True, "250", "259"))
        logger.info(NetworkSettingsView()
        .verify_error_amount("1", True, "4094"))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_verify_start_ip(self):
        PoteenLogger.add_test_case(
            "Check CIDR field validation")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().
        click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().
        select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            (" ", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.10.-1.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.-100.240.255/15 ", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.256.240.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.750.240.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.01.240.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.000.240.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.50.240.255.45/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.240.255/15 ", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.1000.240.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0..240.255/15", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("0.10.100.255/15", True))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_check_cidr_prefix(self):
        PoteenLogger.add_test_case(
            "Check CIDR prefix")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().
        click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().
        select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/1", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/-10", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/0 ", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/31", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/75", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/test", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/", False))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/2", True))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/30", True))
        logger.info(NetworkSettingsView().verify_cidr_vm_networks
            ("240.0.1.0/15", True))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_check_vlan_id_validation(self):
        PoteenLogger.add_test_case(
            "Check VlanID field validation")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().
        click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().
        select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE
        ))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().set_VLAN_manager("on"))
        logger.info(NetworkSettingsView()
        .verify_error_amount("10", True, "250", "259"))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("0", False))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("4095", False))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("-100", False))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("5000", False))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("1", True))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("4094", True))
        logger.info(NetworkSettingsView()
        .verify_vlan_id_range_start("2000", True))
