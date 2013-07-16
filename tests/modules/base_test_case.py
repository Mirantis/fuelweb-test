from engine.poteen.contextHolder import ContextHolder
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen
from devops.helpers.helpers import wait
from ..ci.ci_fuel_web import CiFuelWeb
from ..ci.nailgun_client import NailgunClient

from tests.components.functionality.cluster.browseView \
    import Cluster_BrowseView
from tests.components.functionality.cluster.cluster import Cluster
from tests.components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from tests.components.functionality.cluster.dialogs.deployChangesDialog \
    import DeployChangesDialog
from tests.components.functionality.cluster.editView import Cluster_View
from tests.components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from tests.components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View
from tests.components.settings \
    import DEFAULT_DEPLOYMENT_TIMEOUT_UI, OPENSTACK_CURRENT_VERSION

logger = PoteenLogger


class BaseTestCase(TestCasePoteen):

    def setUp(self):
        super(BaseTestCase, self).setUp()

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
        if not hasattr(self, 'VM_INITIALIZED'):
            self.ci().get_empty_state()
            self.client = NailgunClient(self.get_admin_node_ip())
            ContextHolder.set_url(
                'http://{ip}:{port}'.format(
                    ip=self.get_admin_node_ip(), port=8000))
            self.VM_INITIALIZED = True

        for node in devops_nodes:
            node.start()
        wait(lambda: all(self.nailgun_nodes(devops_nodes)), 15, timeout)
        return self.nailgun_nodes(devops_nodes)

    def create_environment(self, cluster_name, cluster_key='cluster_key',
                           mode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
                           clear_all=True):
        if clear_all:
            logger.info(Cluster_BrowseView().remove_all())
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))
        logger.info(Cluster_Nodes_View().select_environment_mode(
            deploymentMode=mode
        ))

    def add_nodes(self, controllers=0, computes=0, cinders=0):
        if controllers > 0:
            logger.info(Cluster_Nodes_View().click_add_controller())

            available_nodes_names = Cluster_Nodes_ListView()\
                .get_nodes_names_by_status('Discovered')

            logger.info(Cluster_Nodes_ListView().select_nodes(
                *available_nodes_names[:controllers]
            ))
            logger.info(Cluster_Nodes_View().verify_controller_nodes(
                *available_nodes_names[:controllers]
            ))

        if computes > 0:
            logger.info(Cluster_Nodes_View().click_add_compute())

            available_nodes_names = Cluster_Nodes_ListView()\
                .get_nodes_names_by_status('Discovered')

            logger.info(Cluster_Nodes_ListView().select_nodes(
                *available_nodes_names[:computes]
            ))
            logger.info(Cluster_Nodes_View().verify_compute_nodes(
                *available_nodes_names[:computes]
            ))

        if cinders > 0:
            logger.info(Cluster_Nodes_View().click_add_cinder())

            available_nodes_names = Cluster_Nodes_ListView()\
                .get_nodes_names_by_status('Discovered')

            logger.info(Cluster_Nodes_ListView().select_nodes(
                *available_nodes_names[:cinders]
            ))
            logger.info(Cluster_Nodes_View().verify_cinder_nodes(
                *available_nodes_names[:cinders]
            ))

    def deploy_changes(self):
        logger.info(Cluster_View().click_deploy_changes())
        logger.info(DeployChangesDialog().deploy())
        logger.info(Cluster_View().wait_deployment_done(
            DEFAULT_DEPLOYMENT_TIMEOUT_UI
        ))
