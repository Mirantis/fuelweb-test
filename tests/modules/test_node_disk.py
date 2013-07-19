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

logger = PoteenLogger


class TestDeploymentDisks(TestCasePoteen):
    @classmethod
    def setUpClass(cls):
        super(TestDeploymentDisks, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster disks")

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_controller_disk(self):
        PoteenLogger.add_test_case(
            "Controller disk")

        cluster_key = "cluster"
        cluster_name = "Test controller disk"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        # add controller node
        logger.info(Cluster_Nodes_View().click_add_controller())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            available_nodes_names[-1]
        ))
        logger.info(Cluster_Nodes_View().verify_controller_nodes(
            available_nodes_names[-1]
        ))

        # navigate to disks configuration page
        logger.info(
            Cluster_Nodes_View().get_nodes_controllers()[-1].click_hardware())
        logger.info(NodeHardwareDialog().click_disk_configuration())

        # verify default disks settings
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Base System'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').make_bootable.find().verify_attribute(
                'disabled', 'true'))

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

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_compute_disk(self):
        PoteenLogger.add_test_case(
            "Compute disk")

        cluster_key = "cluster"
        cluster_name = "Test compute disk"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        # add compute node
        logger.info(Cluster_Nodes_View().click_add_compute())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            available_nodes_names[-1]
        ))
        logger.info(Cluster_Nodes_View().verify_compute_nodes(
            available_nodes_names[-1]
        ))

        # navigate to disks configuration page
        logger.info(
            Cluster_Nodes_View().get_nodes_computes()[-1].click_hardware())
        logger.info(NodeHardwareDialog().click_disk_configuration())

        # verify default disks settings
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Base System'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Virtual Storage'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').make_bootable.find().verify_attribute(
                'disabled', 'true'))

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

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_cinder_disk(self):
        PoteenLogger.add_test_case(
            "Cinder disk")

        cluster_key = "cluster"
        cluster_name = "Test cinder disk"

        logger.info(Main().navigate())
        logger.info(Cluster_BrowseView().remove_all())

        # create cluster
        logger.info(Cluster_BrowseView().click_add_new_cluster(cluster_key))
        logger.info(CreateEnvironmentDialog().populate(
            name=cluster_name,
            version=OPENSTACK_CURRENT_VERSION,
            submit=True
        ))
        logger.info(Cluster_BrowseView().select_by_key(cluster_key))

        # add cinder node
        logger.info(Cluster_Nodes_View().click_add_cinder())
        available_nodes_names = Cluster_Nodes_ListView()\
            .get_nodes_names_by_status('Discovered')
        logger.info(Cluster_Nodes_ListView().select_nodes(
            available_nodes_names[-1]
        ))
        logger.info(Cluster_Nodes_View().verify_cinder_nodes(
            available_nodes_names[-1]
        ))

        # navigate to disks configuration page
        logger.info(
            Cluster_Nodes_View().get_nodes_computes()[-1].click_hardware())
        logger.info(NodeHardwareDialog().click_disk_configuration())

        # verify default disks settings
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Base System'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').verify_volume_size_is_identical('Cinder'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').make_bootable.find().verify_attribute(
                'disabled', 'true'))

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
