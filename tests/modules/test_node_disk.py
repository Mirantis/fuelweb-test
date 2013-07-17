from nose.plugins.attrib import attr

from engine.poteen.poteenLogger import PoteenLogger

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
from base_test_case import BaseTestCase

logger = PoteenLogger


class TestDeploymentDisks(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDeploymentDisks, cls).setUpClass()
        PoteenLogger.add_test_suite("Cluster deployment")

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

        self.verify_bottom_buttons()
        self.verify_disk_boxes({
            'sda': {'Base System': {'btn_close': False}},
            'sdb': {'Base System': {'btn_close': True}}})

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

        self.verify_bottom_buttons()
        self.verify_disk_boxes({
            'sda': {'Base System': {'btn_close': False},
                    'Virtual Storage': {'btn_close': True}},
            'sdb': {'Virtual Storage': {'btn_close': True}}})

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

        self.verify_bottom_buttons()
        self.verify_disk_boxes({
            'sda': {'Base System': {'btn_close': False},
                    'Cinder': {'btn_close': True}},
            'sdb': {'Cinder': {'btn_close': True}}})

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_buttons_interactions(self):
        PoteenLogger.add_test_case(
            "Buttons interactions")

        cluster_key = "cluster"
        cluster_name = "Test buttons interactions"

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
        self.verify_bottom_buttons()
        logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').size.set_value('11.51'))
        self.verify_bottom_buttons(apply=None, cancel=None)
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').use_all_unallocated.click())
        self.verify_bottom_buttons()

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_load_defaults_cancel(self):
        PoteenLogger.add_test_case(
            "Load defaults")

        cluster_key = "cluster"
        cluster_name = "Load defaults"

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

        # test load defaults
        logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').size.set_value('11.51'))
        logger.info(ConfigureDisks().loadDefaults.find().click_and_wait())
        logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').size.verify_value('15.51'))
        self.verify_bottom_buttons()

        # test cancel
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').size.set_value('10.12'))
        logger.info(ConfigureDisks().cancelChanges.find().click_and_wait())
        logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').size.verify_value('15.51'))
        self.verify_bottom_buttons()

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_remove_volume_group(self):
        PoteenLogger.add_test_case(
            "Remove volume group")

        cluster_key = "cluster"
        cluster_name = "Remove volume group"

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

        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box('sda').get_volume_group(
            'Cinder').close.click_and_wait())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group_box('Cinder').size.verify_value('0.00'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group('Cinder').size.verify_value('0.00 GB'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group('Unallocated').size.verify_value('300.46 GB'))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_error_message(self):
        PoteenLogger.add_test_case(
            "Error message")

        cluster_key = "cluster"
        cluster_name = "Error message"

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

        # Maximal size error message
        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group_box('Cinder').size.set_value('350.00'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group_box('Cinder').size.verify_attribute(
                'class', 'input-mini error'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').error_message.find(text='Maximal size').verify_value(
                'Maximal size is 300.47 GB'))

        # Minimal size error message
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group_box('Base System').size.set_value('12.00'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').get_volume_group_box('Base System').size.verify_attribute(
                'class', 'input-mini error'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').error_message.find(text='Minimal size').verify_value(
                'Minimal size is 18.59 GB'))

    @attr(env=["fakeui"], set=["smoke", "regression", "full"])
    def test_make_bootable(self):
        PoteenLogger.add_test_case(
            "Make bootable")

        cluster_key = "cluster"
        cluster_name = "Make bootable"

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

        logger.info(ConfigureDisks().get_disk_box('sda').click_disk_map())
        logger.info(ConfigureDisks().get_disk_box('sdb').click_disk_map())

        logger.info(ConfigureDisks().get_disk_box(
            'sdb').make_bootable.verify_attribute('disabled', 'true'))
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').get_volume_group_box('Cinder').size.set_value('10.00'))
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').make_bootable.verify_attribute('disabled', None))

        # make bootable another disk
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').make_bootable.click())

        logger.info(ConfigureDisks().get_disk_box(
            'sda').make_bootable.verify_attribute('disabled', None))
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').make_bootable.verify_attribute('disabled', 'true'))

        logger.info(ConfigureDisks().get_disk_box(
            'sda').bootable_marker.verify_attribute(
                'style', 'display: none;'))
        logger.info(ConfigureDisks().get_disk_box(
            'sdb').bootable_marker.verify_attribute(
                'style', 'display: inline;'))

        # make bootable the first disk
        logger.info(ConfigureDisks().get_disk_box(
            'sda').make_bootable.click())

        logger.info(ConfigureDisks().get_disk_box(
            'sdb').make_bootable.verify_attribute('disabled', None))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').make_bootable.verify_attribute('disabled', 'true'))

        logger.info(ConfigureDisks().get_disk_box(
            'sdb').bootable_marker.verify_attribute(
                'style', 'display: none;'))
        logger.info(ConfigureDisks().get_disk_box(
            'sda').bootable_marker.verify_attribute(
                'style', 'display: inline;'))

    def verify_bottom_buttons(self, load_defaults=None,
                              apply='true', cancel='true', back_to_node=None):
        logger.info(ConfigureDisks().loadDefaults.find().verify_attribute(
            'disabled', load_defaults))
        logger.info(ConfigureDisks().applyButton.find().verify_attribute(
            'disabled', apply))
        logger.info(ConfigureDisks().cancelChanges.find().verify_attribute(
            'disabled', cancel))
        logger.info(ConfigureDisks().backToNodeList.find().verify_attribute(
            'disabled', back_to_node))

    def verify_disk_box(self, disk_name, boxes):
        for bn, info in boxes.iteritems():
            logger.info(ConfigureDisks().get_disk_box(
                disk_name).get_volume_group(bn).close.find().verify_attribute(
                    'class', 'close-btn hide'))

        logger.info(ConfigureDisks().get_disk_box(disk_name).click_disk_map())

        for bn, info in boxes.iteritems():
            logger.info(ConfigureDisks().get_disk_box(
                disk_name).verify_volume_size_is_identical(bn))
            logger.info(ConfigureDisks().get_disk_box(
                disk_name).make_bootable.find().verify_attribute(
                    'disabled', 'true'))

            close_btn_class_attr = 'close-btn' if info['btn_close'] \
                else 'close-btn hide'
            logger.info(ConfigureDisks().get_disk_box(
                disk_name).get_volume_group(bn).close.find().verify_attribute(
                    'class', close_btn_class_attr))

    def verify_disk_boxes(self, info):
        for disk_name, boxes_info in info.iteritems():
            self.verify_disk_box(disk_name, boxes_info)