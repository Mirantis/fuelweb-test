from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.radio import Radio
from engine.poteen.elements.basic.select import Select
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
            xpath=".//input[@value='FlatDHCPManager']",
            element_name="FlatDHCP Manager")

        self.vlan_manager = Radio(
            xpath=".//input[@value='VlanManager']",
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
            xpath=".//div[contains(@class, 'btn-revert-changes')]",
            element_name="Cancel changes"
        )
        self.save_settings = Button(
            xpath=".//div[contains(@class, 'btn-success apply-btn')]",
            element_name="Save settings"
        )

        AbstractView.__init__(self, parent)

    def get_ip_range_row(self, name, num):
        return IpRangeRow(self.ip_range_row.find(name=name, num=num))
