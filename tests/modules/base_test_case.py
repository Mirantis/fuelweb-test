from engine.poteen.contextHolder import ContextHolder
from engine.poteen.testCasePoteen import TestCasePoteen
from devops.helpers.helpers import wait
from ..ci.ci_fuel_web import CiFuelWeb
from ..ci.nailgun_client import NailgunClient


class BaseTestCase(TestCasePoteen):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.ci().get_empty_state()
        self.client = NailgunClient(self.get_admin_node_ip())
        ContextHolder.set_url(
            'http://{ip}:{port}'.format(
                ip=self.get_admin_node_ip(), port=8000))

    def ci(self):
        if not hasattr(self, '_ci'):
            self._ci = CiFuelWeb()
        return self._ci

    def nailgun_nodes(self, devops_nodes):
        return map(lambda node: self.get_node_by_devops_node(node),
                   devops_nodes)

    def get_admin_node_ip(self):
        return str(
            self.ci().nodes().admin.get_ip_address_by_network_name('internal'))

    def get_node_by_devops_node(self, devops_node):
        """Returns dict with nailgun slave node description if node is
        registered. Otherwise return None.
        """
        mac_addresses = map(
            lambda interface: interface.mac_address.capitalize(),
            devops_node.interfaces)
        for nailgun_node in self.client.list_nodes():
            if nailgun_node['mac'].capitalize() in mac_addresses:
                nailgun_node['devops_name'] = devops_node.name
                return nailgun_node
        return None

    def bootstrap_nodes(self, devops_nodes, timeout=600):
        """Start vms and wait they are registered on nailgun.
        :rtype : List of registred nailgun nodes
        """
        for node in devops_nodes:
            node.start()
        wait(lambda: all(self.nailgun_nodes(devops_nodes)), 15, timeout)
        return self.nailgun_nodes(devops_nodes)