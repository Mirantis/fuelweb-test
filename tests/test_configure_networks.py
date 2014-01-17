import time
from selenium.webdriver import ActionChains
import browser
from pageobjects.environments import Environments
from pageobjects.node_interfaces_settings import Settings
from pageobjects.nodes import Nodes, RolesPanel, NodeInfo
from pageobjects.tabs import Tabs
from tests import preconditions
from tests.base import BaseTestCase


class TestConfigureNetworksPage(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        preconditions.Environment.simple_flat()
        Environments().create_cluster_boxes[0].click()
        Nodes().add_nodes.click()
        time.sleep(1)
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().controller.click()
        Nodes().apply_changes.click()

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        Nodes().nodes[0].details.click()
        NodeInfo().edit_networks.click()
        time.sleep(1)

    def test_drag_and_drop(self):
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['storage'],
                s.interfaces[1].networks_box).perform()
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['management'],
                s.interfaces[2].networks_box).perform()
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['vm (fixed)'],
                s.interfaces[2].networks_box).perform()

            self.assertIn(
                'storage', s.interfaces[1].networks,
                'storage at eht1')
            self.assertIn(
                'management', s.interfaces[2].networks,
                'management at eht2')
            self.assertIn(
                'vm (fixed)', s.interfaces[2].networks,
                'vm (fixed) at eht2')

    def test_public_floating_grouped(self):
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['public'],
                s.interfaces[1].networks_box).perform()
            self.assertIn(
                'floating', s.interfaces[1].networks,
                'Floating has been moved')
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[1].networks['floating'],
                s.interfaces[2].networks_box).perform()
            self.assertIn(
                'public', s.interfaces[2].networks,
                'Public has been moved')

    def test_admin_pxe_is_not_dragable(self):
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[2].networks['admin (pxe)'],
                s.interfaces[0].networks_box).perform()
            self.assertNotIn(
                'admin (pxe)', s.interfaces[1].networks,
                'admin (pxe) has not been moved')

    def test_two_untagged_on_interface(self):
        error = 'Untagged networks can not be assigned to one interface'
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['public'],
                s.interfaces[2].networks_box).perform()
            self.assertIn(
                'nodrag', s.interfaces[2].parent.get_attribute('class'),
                'Red border')
            self.assertIn(
                error, s.interfaces[2].parent.find_element_by_xpath('./..').text,
                'Error message is displayed'
            )
            self.assertFalse(s.apply.is_enabled(), 'Apply disabled')
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[2].networks['public'],
                s.interfaces[1].networks_box).perform()
            self.assertNotIn(
                'nodrag', s.interfaces[2].parent.get_attribute('class'),
                'Red border')
            self.assertNotIn(
                error, s.interfaces[2].parent.find_element_by_xpath('./..').text,
                'Error message is displayed'
            )
            self.assertTrue(s.apply.is_enabled(), 'Apply enabled')

    def test_cancel_changes(self):
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['public'],
                s.interfaces[1].networks_box).perform()
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['storage'],
                s.interfaces[2].networks_box).perform()

            s.cancel_changes.click()
            time.sleep(1)
            self.assertIn(
                'storage', s.interfaces[0].networks,
                'storage at eht0')
            self.assertIn(
                'public', s.interfaces[0].networks,
                'public at eht0')
            self.assertIn(
                'floating', s.interfaces[0].networks,
                'floating at eht0')


class TestConfigureNetworks(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()

    def setUp(self):
        BaseTestCase.clear_nailgun_database()
        BaseTestCase.setUp(self)

        preconditions.Environment.simple_flat()
        Environments().create_cluster_boxes[0].click()
        Nodes().add_nodes.click()
        time.sleep(1)
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().controller.click()
        Nodes().apply_changes.click()
        time.sleep(1)
        Nodes().nodes[0].details.click()
        NodeInfo().edit_networks.click()
        time.sleep(1)

    def test_save_load_defaults(self):
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['public'],
                s.interfaces[1].networks_box).perform()
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['storage'],
                s.interfaces[2].networks_box).perform()
            s.apply.click()
            time.sleep(1)
        self.refresh()
        with Settings() as s:
            self.assertIn(
                'storage', s.interfaces[2].networks,
                'storage at eht2')
            self.assertIn(
                'public', s.interfaces[1].networks,
                'public at eht1')
            self.assertIn(
                'floating', s.interfaces[1].networks,
                'floating at eht1')
            s.load_defaults.click()
            time.sleep(1)
            self.assertIn(
                'storage', s.interfaces[0].networks,
                'storage at eht0')
            self.assertIn(
                'public', s.interfaces[0].networks,
                'public at eht0')
            self.assertIn(
                'floating', s.interfaces[0].networks,
                'floating at eht0')

    def test_configure_interfaces_of_several_nodes(self):
        # Go back to nodes page
        Tabs().nodes.click()
        time.sleep(1)
        # Add second node
        Nodes().add_nodes.click()
        time.sleep(1)
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().compute.click()
        Nodes().apply_changes.click()
        time.sleep(1)
        # rearrange interfaces
        with Nodes() as n:
            n.select_all.click()
            n.configure_interfaces.click()
            time.sleep(1)
        with Settings() as s:
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['public'],
                s.interfaces[1].networks_box).perform()
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['management'],
                s.interfaces[1].networks_box).perform()
            ActionChains(browser.driver).drag_and_drop(
                s.interfaces[0].networks['storage'],
                s.interfaces[2].networks_box).perform()
            s.apply.click()
            time.sleep(1)

        for i in range(2):
            # Go to nodes page
            Tabs().nodes.click()
            time.sleep(1)
            # Verify interfaces settings of each node
            Nodes().nodes[i].details.click()
            NodeInfo().edit_networks.click()
            time.sleep(1)
            self.assertIn(
                'public', s.interfaces[1].networks,
                'public at eht1. Node #{0}'.format(i))
            self.assertIn(
                'management', s.interfaces[1].networks,
                'management at eht1. Node #{0}'.format(i))
            self.assertIn(
                'storage', s.interfaces[2].networks,
                'storage at eht2. Node #{0}'.format(i))
