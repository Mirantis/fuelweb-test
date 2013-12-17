from selenium.webdriver.support.select import Select
from pageobjects.base import PageObject


class Settings(PageObject):

    @property
    def install_savanna(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('savanna'))

    @property
    def install_murano(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('murano'))

    @property
    def install_ceilometer(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('ceilometer'))

    @property
    def hypervisor_kvm(self):
        return self.parent.find_element_by_xpath(self.XPATH_RADIO.format('libvirt_type', 'kvm'))

    @property
    def hypervisor_qemu(self):
        return self.parent.find_element_by_xpath(self.XPATH_RADIO.format('libvirt_type', 'qemu'))

    @property
    def cinder_for_volumes(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('volumes_lvm'))

    @property
    def ceph_for_volumes(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('volumes_ceph'))

    @property
    def ceph_for_images(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('images_ceph'))

    @property
    def ceph_rados_gw(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('objects_ceph'))

    @property
    def install_savanna(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('savanna'))

    @property
    def install_murano(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('murano'))

    @property
    def install_ceilometer(self):
        return self.parent.find_element_by_xpath(self.XPATH_CHECKBOX.format('ceilometer'))