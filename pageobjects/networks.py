from selenium.webdriver.support.select import Select
from fuelui_tests.pageobjects.base import PageObject


class Networks(PageObject):

    @property
    def flatdhcp_manager(self):
        return self.parent.find_element_by_xpath(self.XPATH_RADIO.format('net-manager', 'FlatDHCPManager'))

    @property
    def vlan_manager(self):
        return self.parent.find_element_by_xpath(self.XPATH_RADIO.format('net-manager', 'VlanManager'))
