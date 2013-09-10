from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from nose.plugins.attrib import attr

from ..components.settings import OPENSTACK_CURRENT_VERSION
from ..components.functionality.cluster.network_settings.view \
    import NetworkSettingsView
from ..components.functionality.main import Main
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.editView import Cluster_View


logger = PoteenLogger


class Test_Network_settings(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(Test_Network_settings, cls).setUpClass()
        PoteenLogger.add_test_suite("Network validation")

    @attr(set=["smoke", "regression"])
    def test_form(self):
        PoteenLogger.add_test_case(
            "Check network settings page")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode='Multi-node',
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("on"))
        logger.info(NetworkSettingsView().verify_VLAN_manager_value("off"))
        logger.info(NetworkSettingsView().verify_amount_of_blocks(5))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().cancel_changes.get_element(),
            'true', "Cancel changes button"))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().save_settings.get_element(),
            'true', "Save settings button"))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().verify_networks.get_element(),
            None, "Verify networks button"))
        default_value = NetworkSettingsView().vm_networks_cidr.get_value()
        logger.info(
            NetworkSettingsView().vm_networks_cidr.set_value("240.0.1.0/25"))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().save_settings.get_element(),
            None, "Save settings button"))
        logger.info(
            NetworkSettingsView().vm_networks_cidr.set_value(default_value))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().save_settings.get_element(),
            'true', "Save settings button"))

    @attr(set=["smoke", "regression"])
    def test_change_network(self):
        PoteenLogger.add_test_case(
            "Change network manager")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode='Multi-node',
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("on"))
        logger.info(NetworkSettingsView().verify_VLAN_manager_value("off"))
        logger.info(
            NetworkSettingsView().verify_visibility_vlan_manager_fields(False))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().save_settings.get_element(),
            'true', "Save settings button"))
        logger.info(NetworkSettingsView().set_VLAN_manager("on"))
        logger.info(NetworkSettingsView().verify_flatDHCP_manager_value("off"))
        logger.info(VerifyBot().verify_disabled(
            NetworkSettingsView().save_settings.get_element(),
            None, "Save settings button"))
        logger.info(
            NetworkSettingsView().verify_visibility_vlan_manager_fields(True))
        logger.info(NetworkSettingsView().set_flatDHCP_manager("on"))
        logger.info(NetworkSettingsView().verify_VLAN_manager_value("off"))
        logger.info(
            NetworkSettingsView().verify_visibility_vlan_manager_fields(False))

    @attr(set=["smoke", "regression"])
    def test_amount_field_validation(self):
        PoteenLogger.add_test_case(
            "Check Amount field validation")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode='Multi-node',
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().set_VLAN_manager("on"))
        amount_array = [
            (" ", False),
            ("-10", False),
            ("0", False)
        ]
        for amount, valid in amount_array:
            logger.info(
                NetworkSettingsView().verify_error_amount(amount, valid))
        logger.info(
            NetworkSettingsView().verify_error_amount("2", False, "4094"))
        amount_array = [
            ("2", True, "4093", "4094"),
            ("4094", True, "1", "4094"),
            ("10", True, "250", "259")]
        for amount, valid, start_ip, end_ip in amount_array:
            logger.info(
                NetworkSettingsView().verify_error_amount(
                    amount, valid, start_ip, end_ip))
        logger.info(
            NetworkSettingsView().verify_error_amount("1", True, "4094"))

    @attr(set=["smoke", "regression"])
    def test_verify_start_ip(self):
        PoteenLogger.add_test_case(
            "Check CIDR field validation")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode='Multi-node',
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_View().click_network_settings_tab())
        cidr_vm_networks = [
            (" ", False),
            ("0.10.-1.255/15", False),
            ("0.-100.240.255/15 ", False),
            ("0.256.240.255/15", False),
            ("0.750.240.255/15", False),
            ("0.01.240.255/15", False),
            ("0.000.240.255/15", False),
            ("0.50.240.255.45/15", False),
            ("0.240.255/15 ", False),
            ("0.1000.240.255/15", False),
            ("0..240.255/15", False),
            ("0.10.100.255/15", True)]
        for cidr_vm_network, valid in cidr_vm_networks:
            logger.info(
                NetworkSettingsView().verify_cidr_vm_networks(
                    cidr_vm_network, valid))

    @attr(set=["smoke", "regression"])
    def test_check_cidr_prefix(self):
        PoteenLogger.add_test_case(
            "Check CIDR prefix")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode='Multi-node',
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        logger.info(Cluster_View().click_network_settings_tab())
        cidr_vm_networks = [
            ("240.0.1.0/1", False),
            ("240.0.1.0/-10", False),
            ("240.0.1.0/0 ", False),
            ("240.0.1.0/31", False),
            ("240.0.1.0/75", False),
            ("240.0.1.0/test", False),
            ("240.0.1.0/", False),
            ("240.0.1.0/2", True),
            ("240.0.1.0/30", True),
            ("240.0.1.0/15", True)
        ]
        for cidr_vm_network, valid in cidr_vm_networks:
            logger.info(
                NetworkSettingsView().verify_cidr_vm_networks(
                    cidr_vm_network, valid))

    @attr(set=["smoke", "regression"])
    def test_check_vlan_id_validation(self):
        PoteenLogger.add_test_case(
            "Check VlanID field validation")

        cluster_key = "cluster"
        cluster_name = "Test environment"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().createEnvironment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode='Multi-node',
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_View().click_network_settings_tab())
        logger.info(NetworkSettingsView().set_VLAN_manager("on"))
        logger.info(
            NetworkSettingsView().verify_error_amount(
                "10", True, "250", "259"))
        vlan_id_range_start_array = [
            ("0", False),
            ("4095", False),
            ("-100", False),
            ("5000", False),
            ("1", True),
            ("4094", True),
            ("2000", True)]
        for vlan_id_range_start, valid in vlan_id_range_start_array:
            logger.info(
                NetworkSettingsView().verify_vlan_id_range_start(
                    vlan_id_range_start, valid))
