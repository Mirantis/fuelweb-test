import time
from fuelui_tests.pageobjects.environments import Environments, Wizard
from fuelui_tests.pageobjects.networks import Networks
from fuelui_tests.pageobjects.nodes import Nodes
from fuelui_tests.pageobjects.settings import Settings
from fuelui_tests.pageobjects.tabs import Tabs
from fuelui_tests.settings import *
from fuelui_tests.tests.base import BaseTestCase


class TestEnvironment(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_box.click()
        time.sleep(2)

    def test_centos_simple(self):
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(6):
                w.next.click()
            w.create.click()
            time.sleep(2)

        cb = Environments().create_cluster_boxes[0]
        self.assertIn(OPENSTACK_CENTOS, cb.text)
        cb.click()

        with Nodes() as n:
            self.assertEqual(n.env_name.text, OPENSTACK_CENTOS)
            n.info_icon.click()
            self.assertIn('display: block;', n.env_details.get_attribute('style'))
            self.assertIn(OPENSTACK_CENTOS, n.env_details.text)
            self.assertIn('New', n.env_details.text)
            self.assertIn('Multi-node', n.env_details.text)
            n.info_icon.click()
            self.assertIn('display: none;', n.env_details.get_attribute('style'))
        Tabs().networks.click()
        with Networks() as n:
            self.assertTrue(n.flatdhcp_manager.find_element_by_tag_name('input').is_selected())
        Tabs().settings.click()
        with Settings() as s:
            self.assertFalse(s.install_savanna.find_element_by_tag_name('input').is_selected())
            self.assertFalse(s.install_murano.find_element_by_tag_name('input').is_selected())
            self.assertFalse(s.install_ceilometer.find_element_by_tag_name('input').is_selected())
            self.assertTrue(s.hypervisor_qemu.find_element_by_tag_name('input').is_selected())
        pass