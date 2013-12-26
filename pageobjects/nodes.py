from selenium.webdriver.support.select import Select
import browser
from pageobjects.base import PageObject, Popup


class Nodes(PageObject):

    @property
    def info_icon(self):
        return self.parent.find_element_by_css_selector('i.icon-info-circled')

    @property
    def env_name(self):
        return self.parent.find_element_by_css_selector('span.btn-cluster-details')

    @property
    def env_details(self):
        return self.parent.find_element_by_css_selector('ul.cluster-details')

    @property
    def group_by(self):
        return Select(self.parent.find_element_by_css_selector('select[name=grouping]'))

    @property
    def add_nodes(self):
        return self.parent.find_element_by_css_selector('button.btn-add-nodes')

    @property
    def apply_changes(self):
        return self.parent.find_element_by_css_selector('button.btn-apply')

    @property
    def configure_interfaces(self):
        return self.parent.find_element_by_css_selector('button.btn-configure-interfaces')

    @property
    def configure_disks(self):
        return self.parent.find_element_by_css_selector('button.btn-configure-disks')

    @property
    def nodes_discovered(self):
        elements = self.parent.find_elements_by_css_selector('.node-container.discover')
        return [NodeContainer(el) for el in elements]

    @property
    def nodes_offline(self):
        elements = self.parent.find_elements_by_css_selector('.node-container.node-offline')
        return [NodeContainer(el) for el in elements]

    @property
    def nodes_error(self):
        elements = self.parent.find_elements_by_css_selector('.node-container.error')
        return [NodeContainer(el) for el in elements]


class NodeContainer(PageObject):

    XPATH_BY_STATUS = '//label[contains(@class, "node-container") and ' \
                      './/span[@class="node-status-label"]="{}"]'

    @classmethod
    def find_by_status(cls, status):
        elements = browser.driver.find_element_by_xpath(cls.XPATH_BY_STATUS.format(status))
        return [cls(el) for el in elements]

    @classmethod
    def find_discovered(cls):
        return cls.find_by_status('Discovered')

    @property
    def checkbox(self):
        return self.parent.find_element_by_css_selector('div.node-checkbox')

    @property
    def roles(self):
        return self.parent.find_element_by_css_selector('div.role-list')


class RolesPanel(PageObject):

    XPATH_ROLE = '//label[contains(., "{}")]/input'

    @property
    def controller(self):
        return self.parent.find_element_by_xpath(self.XPATH_ROLE.format('Controller'))

    @property
    def compute(self):
        return self.parent.find_element_by_xpath(self.XPATH_ROLE.format('Compute'))

    @property
    def cinder(self):
        return self.parent.find_element_by_xpath(self.XPATH_ROLE.format('Cinder'))

    @property
    def ceph_osd(self):
        return self.parent.find_element_by_xpath(self.XPATH_ROLE.format('Ceph OSD'))


class NodeInfo(Popup):

    @property
    def edit_networks(self):
        return self.parent.find_element_by_css_selector('.btn-edit-networks')

    @property
    def edit_disks(self):
        return self.parent.find_element_by_css_selector('.btn-edit-disks')
