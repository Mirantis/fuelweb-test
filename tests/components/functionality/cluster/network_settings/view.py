from selenium.webdriver.common.by import By
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.radio import Radio
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.result import Result
from engine.poteen.log.resultList import ResultList
from ....generic.abstractView import AbstractView
from .....components.functionality.cluster.generic.ip_range_row \
    import IpRangeRow


class NetworkSettingsView(AbstractView):
    def __init__(self, parent=None):
        self.save_settings = Button(
            xpath=".//div[contains(@class, 'apply-btn')]",
            element_name="Save Settings")

        self.cancel_changes = Button(
            xpath=".//div[contains(@class, 'btn-revert-changes')]",
            element_name="Cancel Changes")

        self.verify_networks = Button(
            xpath=".//div[contains(@class, 'verify-networks-btn')]",
            element_name="Verify networks")

        self.flat_dhcp_manager = Radio(
            xpath=".//div[@class='custom-tumbler' "
                  "and input[@value='FlatDHCPManager']]",
            element_name="FlatDHCP Manager")

        self.vlan_manager = Radio(
            xpath=".//div[@class='custom-tumbler' "
                  "and input[@value='VlanManager']]",
            element_name="Vlan Manager")

        self.ip_range_row = HtmlElement(
            xpath=".//div[@class='{name}']/"
                  "div[contains(@class,'range-row ')][{num}]",
            element_name="Range row {name} [{num}]")

        self.public_vlan_id = Input(
            xpath=".//input[@name='public-vlan_start']",
            element_name="Public VLAN ID")

        self.public_netmask = Input(
            xpath=".//input[@name='public-netmask']",
            element_name="Public Netmask")

        self.public_gateway = Input(
            xpath=".//input[@name='public-gateway']",
            element_name="Public Gateway")

        self.management_cidr = Input(
            xpath=".//input[@name='management-cidr']",
            element_name="Management CIDR")

        self.management_vlan_id = Input(
            xpath=".//input[@name='management-vlan_start']",
            element_name="Management VLAN ID")

        self.storage_cidr = Input(
            xpath=".//input[@name='storage-cidr']",
            element_name="Storage CIDR")

        self.storage_vlan_id = Input(
            xpath=".//input[@name='storage-vlan_start']",
            element_name="Storage VLAN ID")

        self.vm_networks_cidr = Input(
            xpath=".//input[@name='fixed-cidr']",
            element_name="VM Networks CIDR")

        self.vm_networks_vlan_id = Input(
            xpath=".//input[@name='fixed-vlan_start']",
            element_name="VM Networks VLAN ID")

        self.vm_networks_vlan_id_range_start = Input(
            xpath=".//input[@name='fixed-vlan_range-start']",
            element_name="VM Networks VLAN ID range start")

        self.vm_networks_vlan_id_range_end = Input(
            xpath=".//input[@name='fixed-vlan_range-end']",
            element_name="VM Networks VLAN ID range end")

        self.vm_networks_number_of_networks = Input(
            xpath=".//input[@name='fixed-amount']",
            element_name="VM Networks. Number of networks")

        self.vm_networks_size_of_networks = Select(
            xpath=".//select[@name='fixed-network_size']",
            element_name="VM Networks. Size of networks")

        self.verify_networks = Button(
            xpath=".//button[contains(@class,'verify-networks-btn')]",
            element_name="Verify networks")

        self.cancel_changes = Button(
            xpath=".//button[contains(@class, 'btn-revert-changes')]",
            element_name="Cancel changes"
        )
        self.save_settings = Button(
            xpath=".//button[contains(@class, 'btn-success apply-btn')]",
            element_name="Save settings"
        )

        AbstractView.__init__(self, parent)

    def get_ip_range_row(self, name, num):
        return IpRangeRow(self.ip_range_row.find(name=name, num=num))

    def verify_error(self, obj, args, value, error_class="error",
                     simple_class=""):
        rl = ResultList("Set '{args}' and verify validation"
        .format(args=args)).push(obj.set_value(args))
        if value:
            rl.push(obj.verify_attribute("class", simple_class))
        else:
            rl.push(obj.verify_attribute("class", error_class))
        return rl

    def verify_cidr_vm_networks(self, args, value):
        return self.verify_error(self.vm_networks_cidr, args, value)

    def verify_amount(self, args, value):
        return self.verify_error(self.vm_networks_number_of_networks,
                                 args, value, "range error", "range")

    def verify_vlan_id_range_start(self, args, value):
        return self.verify_error(self.vm_networks_vlan_id_range_start,
                                 args, value, "mini range error", "mini range")

    def verify_error_amount(self, arg_number, value, arg_start_range=1,
                            arg_end_range=None):
        rl = ResultList("Verify validation of field number of networks"
                        " with value '{args}'"
        .format(args=arg_number))
        rl.push(self.vm_networks_vlan_id_range_start.
        set_value(arg_start_range))
        rl.push(self.verify_amount(arg_number, value))
        if arg_end_range is not None:
            rl.push(self.vm_networks_vlan_id_range_end.
            verify_value(arg_end_range))
        return rl

    def set_flatDHCP_manager(self, value):
        return self.flat_dhcp_manager.set_value(value)

    def set_VLAN_manager(self, value):
        return self.vlan_manager.set_value(value)

    def verify_flatDHCP_manager_value(self, value):
        return self.flat_dhcp_manager.verify_value(value)

    def verify_VLAN_manager_value(self, value):
        return self.vlan_manager.verify_value(value)

    def get_networks_blocks(self):
        return self.get_action_bot().find_elements(
            By.XPATH, ".//div/legend[@class='networks']")

    def verify_amount_of_blocks(self, expected_amount):
        status = len(self.get_networks_blocks()) == expected_amount
        return Result(
            "Amount of blocks is {amount}. Amount is equal "
            "with expected: {status}".format(
                amount=len(self.get_networks_blocks()),
                status=status
            ),
            status
        )

    def verify_visibility_vlan_manager_fields(self, value):
        rl = ResultList("Verify vlan manager fields "
                        "are visible: {value}".format(value=value))
        rl.push(VerifyBot().verify_visibility(NetworkSettingsView()
        .vm_networks_number_of_networks.get_element(), value,
                                              "Number of networks"))
        rl.push(VerifyBot().verify_visibility(NetworkSettingsView()
        .vm_networks_size_of_networks.get_element(), value,
                                              "Size of networks"))
        if value:
            rl.push(VerifyBot().verify_visibility(NetworkSettingsView()
                .vm_networks_vlan_id_range_start.get_element(), value,
                                            "Start of VLAN ID range"))
            rl.push(VerifyBot().verify_visibility(NetworkSettingsView()
                .vm_networks_vlan_id_range_end.get_element(), value,
                                                  "End of VLAN ID range"))
        else:
            rl.push(VerifyBot().verify_visibility(NetworkSettingsView()
                .vm_networks_vlan_id_range_start, value,
                                            "Start of VLAN ID range"))
            rl.push(VerifyBot().verify_visibility(NetworkSettingsView()
                .vm_networks_vlan_id_range_end, value, "End of VLAN ID range"))
        return rl
