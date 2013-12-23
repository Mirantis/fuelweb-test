import time
from pageobjects.environments import Environments, Wizard
from pageobjects.networks import Networks
from pageobjects.tabs import Tabs
from settings import *
from tests.base import BaseTestCase

RANGES = [
    ['192.16.0.2', '192.16.0.10'],
    ['192.168.10.20', '192.168.10.50']
]


class BaseClass(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        cls.get_home()
        Environments().create_cluster_box.click()
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(6):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        Tabs().networks.click()

    def _test_ranges_plus_icon(self, network):
        with getattr(Networks(), network) as n:
            n.ip_ranges[0].icon_plus.click()
            self.assertEqual(len(n.ip_ranges), 2, 'Plus icon. row 1')
            n.ip_ranges[1].icon_plus.click()
            self.assertEqual(len(n.ip_ranges), 3, 'Plus icon. row 2')
            n.ip_ranges[1].start.send_keys(RANGES[0][0])
            n.ip_ranges[1].end.send_keys(RANGES[0][1])
            n.ip_ranges[0].icon_plus.click()
            self.assertEqual(len(n.ip_ranges), 4, 'Plus icon. row 1')
            self.assertEqual(n.ip_ranges[1].start.get_attribute('value'), '')
            self.assertEqual(n.ip_ranges[1].end.get_attribute('value'), '')
            self.assertEqual(n.ip_ranges[2].start.get_attribute('value'), RANGES[0][0])
            self.assertEqual(n.ip_ranges[2].end.get_attribute('value'), RANGES[0][1])

    def _test_ranges_minus_icon(self, network):
        with getattr(Networks(), network) as n:
            for i in range(3):
                n.ip_ranges[i].icon_plus.click()
            n.ip_ranges[3].icon_minus.click()
            self.assertEqual(len(n.ip_ranges), 3, 'Minus icon. last row')
            n.ip_ranges[2].start.send_keys(RANGES[0][0])
            n.ip_ranges[2].end.send_keys(RANGES[0][1])
            n.ip_ranges[1].icon_minus.click()
            self.assertEqual(len(n.ip_ranges), 2, 'Minus icon. second row')
            self.assertEqual(n.ip_ranges[1].start.get_attribute('value'), RANGES[0][0])
            self.assertEqual(n.ip_ranges[1].end.get_attribute('value'), RANGES[0][1])

    def _test_use_vlan_tagging(self, network, vlan_id, initial_value=False):
        def assert_on():
            with getattr(Networks(), network) as n:
                self.assertTrue(
                    n.vlan_tagging.find_element_by_tag_name('input').is_selected(),
                    'use vlan tagging is turned on')
                self.assertEqual(n.vlan_id.get_attribute('value'), vlan_id,
                                 'vlan id value')

        def assert_off():
            with getattr(Networks(), network) as n:
                self.assertFalse(
                    n.vlan_tagging.find_element_by_tag_name('input').is_selected(),
                    'use vlan tagging is turned off')
                self.assertFalse(n.vlan_id.is_displayed(),
                                 'vlan id input is not visible')

        def turn_on():
            with getattr(Networks(), network) as n:
                n.vlan_tagging.click()
                self.assertTrue(n.vlan_id.is_displayed(), 'vlan id input is visible')
                n.vlan_id.send_keys(vlan_id)
                Networks().save_settings.click()
                time.sleep(1)
            self.refresh()
            assert_on()

        def turn_off():
            with getattr(Networks(), network) as n:
                n.vlan_tagging.click()
                self.assertFalse(n.vlan_id.is_displayed(),
                                 'vlan id input is not visible')
                Networks().save_settings.click()
                time.sleep(1)
            self.refresh()
            assert_off()

        for i in range(2):
            if initial_value:
                turn_off()
                turn_on()
            else:
                turn_on()
                turn_off()

    def _test_text_field(self, network, field, value):
        with getattr(Networks(), network) as n:
            getattr(n, field).clear()
            getattr(n, field).send_keys(value)
            Networks().save_settings.click()
            time.sleep(1)
        self.refresh()
        with getattr(Networks(), network) as n:
            self.assertEqual(
                getattr(n, field).get_attribute('value'), value,
                'New value')
            getattr(n, field).clear()
            getattr(n, field).send_keys(' ')
            Networks().cancel_changes.click()
            time.sleep(1)
        with getattr(Networks(), network) as n:
            self.assertEqual(
                getattr(n, field).get_attribute('value'), value,
                "cancel changes")


class TestPublicNetwork(BaseClass):

    def test_ranges_plus_icon(self):
        self._test_ranges_plus_icon('public')

    def test_ranges_minus_icon(self):
        self._test_ranges_minus_icon('public')

    def test_use_vlan_tagging(self):
        self._test_use_vlan_tagging('public', '111', False)

    def test_net_mask(self):
        self._test_text_field('public', 'netmask', '255.255.0.0')

    def test_gateway(self):
        self._test_text_field('public', 'gateway', '172.16.0.20')


class TestFloatingNetwork(BaseClass):

    def test_ranges_plus_icon(self):
        self._test_ranges_plus_icon('floating')

    def test_ranges_minus_icon(self):
        self._test_ranges_minus_icon('floating')

    def test_use_vlan_tagging(self):
        value = '112'
        with Networks().public as n:
            n.vlan_tagging.click()
            n.vlan_id.send_keys(value)
        with Networks().floating as n:
            self.assertTrue(
                n.vlan_tagging.find_element_by_tag_name('input').is_selected())
            self.assertEqual(n.vlan_id.get_attribute('value'), value)
        Networks().save_settings.click()
        time.sleep(1)
        self.refresh()
        with Networks().floating as n:
            self.assertTrue(
                n.vlan_tagging.find_element_by_tag_name('input').is_selected())
            self.assertEqual(n.vlan_id.get_attribute('value'), value)
