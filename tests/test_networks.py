import time
from pageobjects.environments import Environments
from pageobjects.networks import Networks
from pageobjects.tabs import Tabs
from tests.base import BaseTestCase
import preconditions

RANGES = [
    ['172.16.0.3', '172.16.0.10'],
    ['172.16.0.20', '172.16.0.50'],
    ['172.16.0.128', '172.16.0.140'],
    ['172.16.0.158', '172.16.0.165']
]


class SimpleFlatNetworks(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        preconditions.Environment.simple_flat()

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        Tabs().networks.click()

    def _assert_save_cancel_disabled(self):
        self.assertFalse(Networks().save_settings.is_enabled(),
                         'Save settings is disabled')
        self.assertFalse(Networks().cancel_changes.is_enabled(),
                         'Cancel changes is disabled')

    def _assert_save_verify_disabled(self):
        self.assertFalse(Networks().save_settings.is_enabled(),
                         'Save settings is disabled')
        self.assertFalse(Networks().verify_networks.is_enabled(),
                         'Verify networks is disabled')

    def _save_settings(self):
        Networks().save_settings.click()
        time.sleep(1)
        self._assert_save_cancel_disabled()
        self.refresh()

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

    def _test_ranges(self, network, values):
        with getattr(Networks(), network) as n:
            n.ip_ranges[0].icon_plus.click()
            n.ip_ranges[0].start.clear()
            n.ip_ranges[0].start.send_keys(values[0][0])
            n.ip_ranges[0].end.clear()
            n.ip_ranges[0].end.send_keys(values[0][1])
            n.ip_ranges[1].start.send_keys(values[1][0])
            n.ip_ranges[1].end.send_keys(values[1][1])
        self._save_settings()
        with getattr(Networks(), network) as n:
            self.assertEqual(n.ip_ranges[0].start.get_attribute('value'), values[0][0])
            self.assertEqual(n.ip_ranges[0].end.get_attribute('value'), values[0][1])
            self.assertEqual(n.ip_ranges[1].start.get_attribute('value'), values[1][0])
            self.assertEqual(n.ip_ranges[1].end.get_attribute('value'), values[1][1])

            n.ip_ranges[0].start.clear()
            n.ip_ranges[0].start.send_keys(' ')
            self.assertIn('Invalid IP range start',
                          n.ip_ranges[0].start.find_element_by_xpath('../../..').text)

            n.ip_ranges[1].end.clear()
            n.ip_ranges[1].end.send_keys(' ')
            self.assertIn('Invalid IP range end',
                          n.ip_ranges[1].end.find_element_by_xpath('../../..').text)

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
                self.assertTrue(n.vlan_id.is_displayed(),
                                'vlan id input is visible')
                n.vlan_id.send_keys(vlan_id)
            self._save_settings()
            assert_on()
            with getattr(Networks(), network) as n:
                n.vlan_id.clear()
                n.vlan_id.send_keys(' ')
                self.assertIn('Invalid VLAN ID',
                              n.vlan_id.find_element_by_xpath('../../..').text)
                self._assert_save_verify_disabled()

        def turn_off():
            with getattr(Networks(), network) as n:
                n.vlan_tagging.click()
                self.assertFalse(n.vlan_id.is_displayed(),
                                 'vlan id input is not visible')
            self._save_settings()
            assert_off()

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
        self._save_settings()
        with getattr(Networks(), network) as n:
            self.assertEqual(
                getattr(n, field).get_attribute('value'), value,
                'New value')
            getattr(n, field).clear()
            getattr(n, field).send_keys(' ')
            self.assertIn('Invalid',
                          getattr(n, field).find_element_by_xpath('../..').text)
            self._assert_save_verify_disabled()
            Networks().cancel_changes.click()
            time.sleep(1)
        with getattr(Networks(), network) as n:
            self.assertEqual(
                getattr(n, field).get_attribute('value'), value,
                "cancel changes")


class TestRangesControls(SimpleFlatNetworks):

    def test_public_plus_icon(self):
        self._test_ranges_plus_icon('public')

    def test_public_minus_icon(self):
        self._test_ranges_minus_icon('public')

    def test_floating_plus_icon(self):
        self._test_ranges_plus_icon('floating')

    def test_floating_minus_icon(self):
        self._test_ranges_minus_icon('floating')


class TestPublicNetwork(SimpleFlatNetworks):

    def test_ranges(self):
        self._test_ranges('public', RANGES[:2])

    def test_use_vlan_tagging(self):
        self._test_use_vlan_tagging('public', '111', False)

    def test_net_mask(self):
        self._test_text_field('public', 'netmask', '255.255.0.0')

    def test_gateway(self):
        self._test_text_field('public', 'gateway', '172.16.0.2')


class TestFloatingNetwork(SimpleFlatNetworks):

    def test_ranges(self):
        self._test_ranges('floating', RANGES[2:4])

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


class TestManagementNetwork(SimpleFlatNetworks):

    def test_cidr(self):
        self._test_text_field('management', 'cidr', '192.169.0.0/16')

    def test_use_vlan_tagging(self):
        self._test_use_vlan_tagging('management', '111', True)


class TestStorageNetwork(SimpleFlatNetworks):

    def test_cidr(self):
        self._test_text_field('storage', 'cidr', '192.170.0.0/16')

    def test_use_vlan_tagging(self):
        self._test_use_vlan_tagging('storage', '111', True)


class TestFixedNetwork(SimpleFlatNetworks):

    def test_cidr(self):
        self._test_text_field('fixed', 'cidr', '10.1.0.0/24')

    def test_use_vlan_tagging(self):
        self._test_use_vlan_tagging('fixed', '111', True)


class TestDnsServers(SimpleFlatNetworks):

    def test_name_servers(self):
        v1 = '8.7.7.7'
        v2 = '8.6.6.6'
        with Networks() as n:
            n.dns1.clear()
            n.dns1.send_keys(v1)
            n.dns2.clear()
            n.dns2.send_keys(v2)
        self._save_settings()
        with Networks() as n:
            self.assertEqual(n.dns1.get_attribute('value'), v1, 'dns1')
            self.assertEqual(n.dns1.get_attribute('value'), v1, 'dns2')
            n.dns1.clear()
            n.dns1.send_keys(' ')
            self.assertIn('Invalid nameserver',
                          n.dns1.find_element_by_xpath('../../..').text)

            n.dns2.clear()
            n.dns2.send_keys(' ')
            self.assertIn('Invalid nameserver',
                          n.dns2.find_element_by_xpath('../../..').text)
            self._assert_save_verify_disabled()

            Networks().cancel_changes.click()
            self.assertEqual(n.dns1.get_attribute('value'), v1,
                             'cancel changes dns1')
            self.assertEqual(n.dns1.get_attribute('value'), v1,
                             'cancel changes dns2')
