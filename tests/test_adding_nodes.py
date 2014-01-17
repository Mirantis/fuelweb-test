import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pageobjects.base import PageObject
from pageobjects.environments import Environments
from pageobjects.nodes import Nodes, NodeInfo, RolesPanel
from tests import preconditions
from tests.base import BaseTestCase
from tests.test_roles import ROLE_CONTROLLER, ROLE_CEPH, ROLE_CINDER


class TestNodesAddPage(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        preconditions.Environment.simple_flat()

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        Nodes().add_nodes.click()
        time.sleep(1)

    def test_discovered_nodes_enabled(self):
        with Nodes()as n:
            for node in n.nodes_discovered:
                self.assertTrue(
                    node.checkbox.find_element_by_tag_name('input').is_enabled(),
                    'Node enabled')

    def test_offline_nodes_disabled(self):
        with Nodes()as n:
            for node in n.nodes_offline:
                self.assertFalse(
                    node.checkbox.find_element_by_tag_name('input').is_enabled(),
                    'Node disabled')

    def test_error_nodes_disabled(self):
        with Nodes()as n:
            for node in n.nodes_error:
                self.assertFalse(
                    node.checkbox.find_element_by_tag_name('input').is_enabled(),
                    'Node disabled')

    def test_select_all(self):
        with Nodes()as n:
            n.select_all.click()
            for selects in n.select_all_in_group:
                self.assertTrue(selects.is_selected(),
                                'Select all in group is selected')
            for node in n.nodes_discovered:
                self.assertTrue(
                    node.checkbox.find_element_by_tag_name('input').is_selected(),
                    'Discovered node is selected')
            for node in n.nodes_offline:
                self.assertFalse(
                    node.checkbox.find_element_by_tag_name('input').is_selected(),
                    'Offline node is not selected')
            for node in n.nodes_error:
                self.assertFalse(
                    node.checkbox.find_element_by_tag_name('input').is_selected(),
                    'Error node is not selected')

    def test_selecting_nodes_clicking_them(self):
        with Nodes()as n:
            for node in n.nodes_discovered:
                node.parent.click()
                self.assertTrue(
                    node.checkbox.find_element_by_tag_name('input').is_selected(),
                    'Discovered node is selected')
            for node in n.nodes_offline:
                node.parent.click()
                self.assertFalse(
                    node.checkbox.find_element_by_tag_name('input').is_selected(),
                    'Offline node is not selected')
            for node in n.nodes_error:
                node.parent.click()
                self.assertFalse(
                    node.checkbox.find_element_by_tag_name('input').is_selected(),
                    'Error node is not selected')

    def test_node_info_popup(self):
        def test_popup(node):
            node.details.click()
            with NodeInfo() as details:
                self.assertEqual(
                    node.name.text, details.header.text,
                    'Node name')
                details.close.click()
                details.wait_until_exists()

        with Nodes()as n:
            test_popup(n.nodes_discovered[0])
            test_popup(n.nodes_offline[0])
            test_popup(n.nodes_error[0])

    def test_renaming_node(self):
        name = 'new node name'
        with Nodes()as n:
            old_name = n.nodes_discovered[0].name.text
            n.nodes_discovered[0].name.click()
            self.assertTrue(
                n.nodes_discovered[0].name_input.is_displayed(),
                'input visible')
            n.nodes_discovered[0].name_input.send_keys(name)
            n.nodes_discovered[0].parent.click()
            self.assertRaises(
                NoSuchElementException, getattr, n.nodes_discovered[0],
                'name_input')
            self.assertEqual(
                old_name, n.nodes_discovered[0].name.text,
                'Node has old name')
            n.nodes_discovered[0].name.click()
            n.nodes_discovered[0].name_input.send_keys(name)
            n.nodes_discovered[0].name_input.send_keys(Keys.ENTER)
            time.sleep(2)
        self.assertEqual(
            name, Nodes().nodes_discovered[0].name.text,
            'New node name')


class TestAddingNodes(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()

    def setUp(self):
        BaseTestCase.clear_nailgun_database()
        preconditions.Environment.simple_flat()
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        Nodes().add_nodes.click()
        time.sleep(1)

    def test_adding_node_single_role(self):
        name = Nodes().nodes_discovered[0].name.text
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().controller.click()
        Nodes().apply_changes.click()
        time.sleep(1)
        with Nodes() as n:
            self.assertTrue(n.env_name.is_displayed())
            self.assertEqual(len(n.nodes), 1, 'Nodes amount')
            self.assertEqual(n.nodes[0].name.text, name, 'Node name')
            self.assertIn(ROLE_CONTROLLER, n.nodes[0].roles.text, 'Node role')

    def test_adding_node_multiple_roles(self):
        Nodes().nodes_discovered[0].checkbox.click()
        with RolesPanel() as r:
            r.controller.click()
            r.cinder.click()
            r.ceph_osd.click()
        Nodes().apply_changes.click()
        time.sleep(1)
        with Nodes() as n:
            self.assertTrue(n.env_name.is_displayed())
            self.assertIn(ROLE_CONTROLLER, n.nodes[0].roles.text,
                          'Node first role')
            self.assertIn(ROLE_CINDER, n.nodes[0].roles.text,
                          'Node second role')
            self.assertIn(ROLE_CEPH, n.nodes[0].roles.text,
                          'Node third role')
