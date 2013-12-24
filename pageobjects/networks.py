from selenium.webdriver.support.select import Select
import browser
from pageobjects.base import PageObject


class Networks(PageObject):


    @property
    def flatdhcp_manager(self):
        return self.parent.find_element_by_xpath(self.XPATH_RADIO.format('net-manager', 'FlatDHCPManager'))

    @property
    def vlan_manager(self):
        return self.parent.find_element_by_xpath(self.XPATH_RADIO.format('net-manager', 'VlanManager'))

    @property
    def segmentation_type(self):
        return self.parent.find_element_by_css_selector('span.network-segment-type')

    @property
    def public(self):
        return Network('Public')

    @property
    def floating(self):
        return Network('Floating')

    @property
    def management(self):
        return Network('Management')

    @property
    def storage(self):
        return Network('Storage')

    @property
    def fixed(self):
        return Network('VM (Fixed)')

    @property
    def neutron(self):
        return NeutronParameters()

    @property
    def dns1(self):
        return self.parent.find_element_by_css_selector('input[name=nameserver-0]')

    @property
    def dns2(self):
        return self.parent.find_element_by_css_selector('input[name=nameserver-1]')

    @property
    def verify_networks(self):
        return self.parent.find_element_by_xpath('//button[text()="Verify Networks"]')

    @property
    def cancel_changes(self):
        return self.parent.find_element_by_xpath('//button[text()="Cancel Changes"]')

    @property
    def save_settings(self):
        return self.parent.find_element_by_xpath('//button[text()="Save Settings"]')


class Network(PageObject):
    XPATH_PARAMETER = './/div[@class="network-attribute" and ' \
                      'div[contains(@class,"parameter-name")]="{}"]'

    XPATH_PARAMETER_RANGES = XPATH_PARAMETER + '/div[contains(@class,"range-row")]'

    def __init__(self, name):
        el = browser.driver.find_element_by_xpath('//div[legend="{}"]'.format(name))
        PageObject.__init__(self, el)

    @property
    def ip_ranges(self):
        elements = self.parent.find_elements_by_xpath(
            self.XPATH_PARAMETER_RANGES.format('IP Range'))
        return [IpRange(el) for el in elements]

    @property
    def vlan_tagging(self):
        return self.parent.find_element_by_css_selector('div.custom-tumbler')

    @property
    def vlan_id(self):
        return self.parent.find_element_by_css_selector('input[name$=vlan_start]')

    @property
    def vlan_end(self):
        return self.parent.find_element_by_css_selector('input[name$=vlan_end]')

    @property
    def netmask(self):
        return self.parent.find_element_by_css_selector('input[name$=netmask]')

    @property
    def gateway(self):
        return self.parent.find_element_by_css_selector('input[name$=gateway]')

    @property
    def cidr(self):
        return self.parent.find_element_by_css_selector('input[name$=cidr]')

    @property
    def number_of_networks(self):
        return self.parent.find_element_by_css_selector('input[name$=amount]')

    @property
    def network_size(self):
        return Select(self.parent.find_element_by_css_selector('select[name$=network_size]'))


class NeutronParameters(PageObject):

    def __init__(self):
        el = browser.driver.find_element_by_css_selector('div.neutron-parameters')
        PageObject.__init__(self, el)

    @property
    def id_start(self):
        return self.parent.find_element_by_css_selector('input[name=id_start]')

    @property
    def id_end(self):
        return self.parent.find_element_by_css_selector('input[name=id_end]')

    @property
    def base_mac(self):
        return self.parent.find_element_by_css_selector('input[name=base_mac]')

    @property
    def floating_start(self):
        return self.parent.find_element_by_css_selector('input[name=floating_start]')

    @property
    def floating_end(self):
        return self.parent.find_element_by_css_selector('input[name=floating_end]')

    @property
    def cidr(self):
        return self.parent.find_element_by_css_selector('input[name=cidr-int]')

    @property
    def gateway(self):
        return self.parent.find_element_by_css_selector('input[name=gateway]')

    @property
    def nameserver0(self):
        return self.parent.find_element_by_css_selector('input[name=nameserver-0]')

    @property
    def nameserver1(self):
        return self.parent.find_element_by_css_selector('input[name=nameserver-1]')


class IpRange(PageObject):

    @property
    def start(self):
        return self.parent.find_element_by_xpath('.//label[1]/div/input')

    @property
    def end(self):
        return self.parent.find_element_by_xpath('.//label[2]/div/input')

    @property
    def icon_plus(self):
        return self.parent.find_element_by_css_selector('i.icon-plus-circle')

    @property
    def icon_minus(self):
        return self.parent.find_element_by_css_selector('i.icon-minus-circle')