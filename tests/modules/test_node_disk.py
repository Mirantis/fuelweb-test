from nose.plugins.attrib import attr
from engine.poteen.poteenLogger import PoteenLogger
from engine.poteen.testCasePoteen import TestCasePoteen

from ..components.functionality.main import Main
from ..components.settings import *
from ..components.functionality.cluster.browseView \
    import Cluster_BrowseView
from ..components.functionality.cluster.dialogs.createEnvironmentDialog \
    import CreateEnvironmentDialog
from ..components.functionality.cluster.nodes.listView \
    import Cluster_Nodes_ListView
from ..components.functionality.cluster.nodes.view \
    import Cluster_Nodes_View
from ..components.functionality.cluster.dialogs.node_hardware_dialog \
    import NodeHardwareDialog
from ..components.functionality.cluster.nodes.configure_disks \
    import ConfigureDisks
from ..components.functionality.cluster.cluster import Cluster

logger = PoteenLogger


class TestDeploymentDisks(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestDeploymentDisks, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster disks")

    @attr(set=["regression"])
    def test_controller_disk(self):
        PoteenLogger.add_test_case(
            "Controller disk")

        cluster_key = "cluster"
        cluster_name = "Test controller disk"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        # add controller node
        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['controller'], [available_nodes_names[-1]]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'controller', [available_nodes_names[-1]]
        ))

        # navigate to disks configuration page
        logger.info(
            Cluster_Nodes_View().get_nodes('controller')[-1].click_hardware())
        logger.info(NodeHardwareDialog().click_disk_configuration())

        # verify default disks settings
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Base System'))

        # logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdb').verify_volume_size_is_identical('Base System'))
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdb').make_bootable.find().verify_attribute('disabled', None))
        #
        # logger.info(ConfigureDisks().get_disk_box('sdc').click_disk_map())
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdc').verify_volume_size_is_identical('Base System'))
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdc').make_bootable.find().verify_attribute('disabled', None))

    @attr(set=["smoke", "regression"])
    def test_compute_disk(self):
        PoteenLogger.add_test_case(
            "Compute disk")

        cluster_key = "cluster"
        cluster_name = "Test compute disk"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            {
                "name": "Test environment",
                "version": OPENSTACK_CURRENT_VERSION,
                "deployment_mode": Cluster.DEPLOYMENT_MODE_MULTI_NODE
            }
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        # add compute node
        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['compute'], [available_nodes_names[-1]]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'compute', [available_nodes_names[-1]]
        ))

        # navigate to disks configuration page
        logger.info(
            Cluster_Nodes_View().get_nodes('compute')[-1].click_hardware())
        logger.info(NodeHardwareDialog().click_disk_configuration())

        # verify default disks settings
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Base System'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Virtual Storage'))

        # logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdb').verify_volume_size_is_identical('Virtual Storage'))
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdb').make_bootable.find().verify_attribute('disabled', None))
        #
        # logger.info(ConfigureDisks().get_disk_box('sdc').click_disk_map())
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdc').verify_volume_size_is_identical('Virtual Storage'))
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdc').make_bootable.find().verify_attribute('disabled', None))

    @attr(set=["regression"])
    @attr("skip")
    def test_cinder_disk(self):
        PoteenLogger.add_test_case(
            "Cinder disk")

        cluster_key = "cluster"
        cluster_name = "Test cinder disk"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().create_environment(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            deploymentMode=Cluster.DEPLOYMENT_MODE_MULTI_NODE,
            computeType='qemu'
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        # add cinder node
        logger.info(Cluster_Nodes_View().click_add_nodes())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_View().assign_roles_to_nodes(
            ['cinder'], [available_nodes_names[-1]]
        ))
        logger.info(Cluster_Nodes_View().verify_nodes(
            'cinder', [available_nodes_names[-1]]
        ))

        # navigate to disks configuration page
        logger.info(
            Cluster_Nodes_View().get_nodes('cinder')[-1].click_hardware())
        logger.info(NodeHardwareDialog().click_disk_configuration())

        # verify default disks settings
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Base System'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Cinder'))

        # logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdb').verify_volume_size_is_identical('Cinder'))
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdb').make_bootable.find().verify_attribute('disabled', None))
        #
        # logger.info(ConfigureDisks().get_disk_box('sdc').click_disk_map())
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdc').verify_volume_size_is_identical('Cinder'))
        # logger.info(ConfigureDisks().get_disk_box(
        #     'sdc').make_bootable.find().verify_attribute('disabled', None))
