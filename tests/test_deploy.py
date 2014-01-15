import time
from pageobjects.base import PageObject
from pageobjects.environments import Environments, DeployChangesPopup
from pageobjects.nodes import Nodes, RolesPanel
from tests import preconditions
from tests.base import BaseTestCase


class TestDeploy(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        preconditions.Environment.simple_flat()

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        time.sleep(1)

    def test_add_nodes(self):
        Nodes().add_nodes.click()
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().controller.click()
        Nodes().apply_changes.click()

        Nodes().add_nodes.click()
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().compute.click()
        Nodes().apply_changes.click()
        time.sleep(1)

        Nodes().deploy_changes.click()
        with DeployChangesPopup() as p:
            p.deploy.click()
            p.wait_until_exists()

        PageObject.wait_until_exists(
            Nodes().progress_deployment, timeout=60)

        with Nodes() as n:
            self.assertEqual(2, len(n.nodes), 'Nodes amount')
            for node in n.nodes:
                self.assertEqual('ready', node.status.text.lower(),
                                 'Node status is READY')


