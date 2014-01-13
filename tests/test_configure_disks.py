import time
from pageobjects.environments import Environments
from pageobjects.node_disks_settings import Settings
from pageobjects.nodes import Nodes, RolesPanel, NodeInfo
from tests import preconditions
from tests.base import BaseTestCase


class TestConfigureDisks(BaseTestCase):

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
        NodeInfo().edit_disks.click()
        time.sleep(1)

    def test_volume_animation(self):
        with Settings() as s:
            s.disks[0].volume_os.parent.click()
            time.sleep(1)
            self.assertTrue(
                s.disks[0].details_panel.is_displayed(),
                'details panel is expanded')

            s.disks[0].volume_os.parent.click()
            time.sleep(1)
            self.assertFalse(
                s.disks[0].details_panel.is_displayed(),
                'details panel is expanded')
