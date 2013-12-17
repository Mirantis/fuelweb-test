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


class NeutronParameters(PageObject):

    def __init__(self):
        PageObject.__init__(self)
        self.parent = browser.driver.find_element_by_css_selector('div.neutron-parameters')